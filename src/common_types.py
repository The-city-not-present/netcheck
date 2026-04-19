


from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import re
import json



def utc_now():
    # return datetime.now(timezone.utc).isoformat(timespec="microseconds")
    return datetime.now(timezone.utc)



@dataclass(kw_only=True)
class CheckResult:
    target: str
    created_at: datetime = field(default_factory=utc_now)
    success: bool
    duration: float | None = None
    error_msg: str | None = None
    response_body: str = field(repr=False)

    @property
    def ok(self) -> bool:
        return self.success

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        duration_formatted = f"{self.duration}"
        try:
            duration_formatted = f"{self.duration*1000:.2f} ms" if duration_formatted is not None else 'None'
        except:
            pass
        response_body = f'{self.response_body}'
        response_body = re.sub(r'\s+',' ',re.sub(r'[\n\r]',' ',response_body))
        if len(response_body)>32:
            response_body = response_body[:30] + '...'
        response_body = json.dumps(response_body)
        error_msg = json.dumps(self.error_msg)
        return (
            f"{cls_name} ( "
            f"target={self.target!r}, "
            f"created_at={self.created_at:%Y-%m-%d %H:%M:%S}, "
            f"success={self.success}, "
            f"duration={duration_formatted}, "
            f"error_msg={error_msg}, "
            f"response_body={response_body}, "
            f" )"
        )

    def as_dict_str_values(self):
        record = {**asdict(self)}

        response_body = record['response_body']
        response_body = f'{response_body}'
        if len(response_body)>64:
            response_body = response_body[:62]+'...'
        response_body = json.dumps(response_body)
        record['response_body'] = response_body

        error_msg = record['error_msg']
        error_msg = f'{error_msg}'
        if len(error_msg)>128:
            error_msg = error_msg[:126]+'...'
        error_msg = json.dumps(error_msg)
        record['error_msg'] = error_msg

        created_at = record['created_at']
        created_at = created_at.isoformat(timespec="microseconds")
        created_at = f'{created_at}'
        record['created_at'] = created_at

        return record
