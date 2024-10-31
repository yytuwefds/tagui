
for n from 1 to 10
  tagui ocr.tag

  if py_result contains "发票不合规"
    fail=get_text(py_result,':','.')
    tagui deliver-fail.tag
  if py_result contains "金额"
    tagui mysql.tag
  wait 2
click (1916,233)


