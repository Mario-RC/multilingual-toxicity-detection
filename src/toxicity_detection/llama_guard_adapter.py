"""Optional Llama Guard-style moderation adapter."""

from __future__ import annotations

from dataclasses import dataclass, field

from toxicity_detection.runtime import resolve_device
from toxicity_detection.schemas import ToxicityCategory, ToxicityResult


LLAMA_GUARD_CATEGORY_MAP = {
    "O1": ToxicityCategory.VIOLENCE_AND_HATE,
    "O2": ToxicityCategory.SEXUAL_EXPLICIT,
    "O3": ToxicityCategory.CRIMINAL_PLANNING,
    "O4": ToxicityCategory.GUNS_AND_ILLEGAL_WEAPONS,
    "O5": ToxicityCategory.REGULATED_OR_CONTROLLED_SUBSTANCES,
    "O6": ToxicityCategory.SELF_HARM,
    "O7": ToxicityCategory.SAFE,
}


@dataclass
class LlamaGuardToxicityDetector:
    model_id: str = "meta-llama/Meta-Llama-Guard-2-8B"
    device: str | None = None
    tokenizer: object = field(init=False, repr=False)
    model: object = field(init=False, repr=False)

    def __post_init__(self) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise ImportError(
                "Llama Guard support is optional. Install it with "
                "`pip install toxicity-detection[llama-guard]`."
            ) from exc

        self.device = resolve_device(self.device)
        dtype = torch.bfloat16 if self.device.startswith("cuda") else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=dtype,
        ).to(self.device)
        self.model.eval()

    def check(self, text: str) -> ToxicityResult:
        import torch

        chat = [{"role": "user", "content": text}]
        input_ids = self.tokenizer.apply_chat_template(chat, return_tensors="pt").to(self.device)
        with torch.no_grad():
            output = self.model.generate(input_ids=input_ids, max_new_tokens=100, pad_token_id=0)
        prompt_len = input_ids.shape[-1]
        result = self.tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)
        category_code = _parse_llama_guard_category(result)
        category = LLAMA_GUARD_CATEGORY_MAP.get(category_code, ToxicityCategory.PROHIBITED_TERM)
        if category == ToxicityCategory.SAFE:
            return ToxicityResult.safe()
        return ToxicityResult.flagged_result(
            category,
            source="llama_guard",
            matched_text=category_code,
        )


def _parse_llama_guard_category(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return "O7"
    if lines[0].lower() == "safe":
        return "O7"
    for line in lines:
        if line.startswith("O") and line[1:].isdigit():
            return line
    return "O7"


LlamaGuardSafetyDetector = LlamaGuardToxicityDetector

