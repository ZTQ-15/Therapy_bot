from pathlib import Path

src = Path(r"C:\Users\vasch\Downloads\moodjournal\frontend-lynx\src\App.jsx")
dst = Path(r"C:\Users\vasch\Downloads\moodjournal\frontend-web\src\App.jsx")

text = src.read_text(encoding="utf-8")
text = text.replace("from '@lynx-js/react';", "from 'react';")
text = text.replace("<scroll-view", "<div").replace("</scroll-view>", "</div>")
text = text.replace("<view", "<div").replace("</view>", "</div>")
text = text.replace("<text", "<span").replace("</text>", "</span>")
text = text.replace("bindtap", "onClick")
text = text.replace("bindinput", "onChange")
text = text.replace("bindfocus", "onFocus")
text = text.replace("show-soft-input-on-focus={true}", "")
text = text.replace("scroll-orientation=\"vertical\"", "")
text = text.replace("scroll-bar-enable={true}", "")
text = text.replace("bounces={true}", "")
text = text.replace("e.detail.value", "e.target.value")

dst.write_text(text, encoding="utf-8")
