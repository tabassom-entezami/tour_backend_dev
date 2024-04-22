import html

from marshmallow import fields, missing


class NullableStr(fields.Str):
    def deserialize(self, *args, **kwargs):
        result = super(NullableStr, self).deserialize(*args, **kwargs)
        if result in ("", None, missing):
            return None
        return result


class SafeString(NullableStr):
    def deserialize(self, *args, **kwargs):
        result = super(SafeString, self).deserialize(*args, **kwargs)
        if result is not None:
            result = html.escape(result, quote=False)
        return result

