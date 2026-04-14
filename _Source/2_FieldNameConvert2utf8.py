import json

# -- 轉換 iso-8859-1 to big5
def Convert_iso8859_to_big5(string):
    s = str(string)
    s = s.encode('iso-8859-1').decode('csbig5')
    return s

# -- 讀入 TableStructure.json
_TableStructure = ''
with open('TableStructure.json', 'r', encoding="utf-8") as f:
    try:
        _TableStructure = json.load(f)
    except Exception as e:
        print(e)
    f.close()

# -- 讀入 language.json
_LANG_JSON = ''
with open('language.json', 'r', encoding="utf-8") as f:
    try:
        _LANG_JSON = json.load(f)
    except Exception as e:
        print(e)
    f.close()
# -- 依據中文 FieldName，查詢其英文欄位名稱 (language.json from TABLE LANGUAGE)
def Get_NameEnglish(chinese_string):
    s = str(chinese_string).strip()

    for item in _LANG_JSON:
        if item.get('CHT') == s:
            if (item.get('ENG') != None):
                return item.get('ENG')
    return s

# -- 因爲這些 Table Name 的 欄位名稱和 Description 都是亂碼
_i_TableID = 'ADMXA,CMSXA,INVXA,PURXA,PURXB,PURXC,MTMXA,MTMXB,MTMXC,MTMXD,MOCXA,MOCXB,MOCXC,VPAXA,VPAXB,VPAXC,VPAXD'

i=0
for item in _TableStructure:
    _TableID = str(item['TableID']).strip()
    # -- 如果 TableID 在 _i_TableID 中，才處理
    for y in _i_TableID.split(','):
        if _TableID == y:
            _FieldName = str(item['FieldName']).strip()
            _Description = str(item['Description']).strip()
            _FieldName_utf8 = Convert_iso8859_to_big5(_FieldName).strip()
            _Description_utf8 = Convert_iso8859_to_big5(_Description).strip()

            # -- 如果 Description 等於 FieldName，Description = ''
            if _Description_utf8 == _FieldName_utf8:
                _Description_utf8 = ''

            _TableStructure[i]['FieldName'] = _FieldName_utf8
            _TableStructure[i]['Description'] = _Description_utf8
            _TableStructure[i]['NameEnglish'] = Get_NameEnglish(_FieldName_utf8)
            
            # -- 如果找到的 NameEnglish 等於 FieldName (都是中文)，NameEnglish = ''
            if _TableStructure[i]['NameEnglish'] == _TableStructure[i]['FieldName']:
                _TableStructure[i]['NameEnglish'] = ''

            break

    i = i + 1

# -- 寫入 TableStructure.json
_jsonData = ''
with open('TableStructure.json', 'w', encoding="utf-8") as fs:
    try:
        _jsonData = json.dumps(_TableStructure, indent=2, ensure_ascii=False)
    except Exception as e:
        print(e)
    fs.write(_jsonData)
    fs.close()

