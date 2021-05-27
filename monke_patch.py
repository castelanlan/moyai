import re
from ast import parse
from inspect import getsource
from discord.gateway import DiscordWebSocket, __dict__


def source(o):
    s = getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(DiscordWebSocket.identify)
source_ = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])', r"\1Discord Android\2", source_
)
m = parse(source_)
loc = {}
exec(compile(m, "<string>", "exec"), __dict__, loc)
DiscordWebSocket.identify = loc["identify"]
