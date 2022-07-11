## Python script to load school banding from schooland web-site (LC20220711)
import time
from datetime import datetime
import urllib
import json
import requests
import ssl
from bs4 import BeautifulSoup

url0='https://www.schooland.hk/ss/'
html0=urllib.request.urlopen(url0, context=ssl._create_unverified_context())
print (f'Status: {html0.status}')
soup0 = BeautifulSoup(html0.read(),features="html5lib")
for s in soup0.select('#contentArea > div:nth-child(6)')[0].find_all('a'):
    print(s.string,url0+s.get('href'))
    cat01=s.string
    url01=url0+s.get('href')
    html01=urllib.request.urlopen(url01, context=ssl._create_unverified_context())
    ## print (f'Status: {html01.status}')
    soup01 = BeautifulSoup(html01.read(),features="html5lib")
    i=0
    for s in soup01.find('table',class_='school-table').find_all('tr'):
        if i>0: print(cat01, s.select('th')[0].string, s.select('td')[4].string)
        i=1

''' Output
港島中西區 https://www.schooland.hk/ss/central-west
港島中西區 聖保羅男女中學 BAND 1
港島中西區 聖保羅書院 BAND 1
港島中西區 聖士提反女子中學 BAND 1
港島中西區 英華女學校 BAND 1
港島中西區 英皇書院 BAND 1
港島中西區 高主教書院 BAND 1
港島中西區 聖嘉勒女書院 BAND 1
港島中西區 聖若瑟書院 BAND 1
港島中西區 聖類斯中學 BAND 1
港島中西區 樂善堂梁銶琚書院 BAND 2
港島中西區 聖士提反堂中學 BAND 2
港島東區 https://www.schooland.hk/ss/eastern
港島東區 庇理羅士女子中學 BAND 1
港島東區 張祝珊英文中學 BAND 1
港島東區 香港中國婦女會中學 BAND 1
港島東區 中華基金中學 BAND 1
港島東區 嘉諾撒書院 BAND 1
港島東區 港島民生書院 BAND 1
港島東區 筲箕灣官立中學 BAND 1
港島東區 聖馬可中學 BAND 1
港島東區 金文泰中學 BAND 1
港島東區 中華傳道會劉永生中學 BAND 1
港島東區 衞理中學 BAND 1
港島東區 培僑中學 BAND 2
港島東區 顯理中學 BAND 2
港島東區 漢華中學 BAND 2
港島東區 伊斯蘭脫維善紀念中學 BAND 2
港島東區 寶血女子中學 BAND 2
港島東區 福建中學小西灣 BAND 2
港島東區 慈幼英文學校 BAND 2
港島東區 香港文理書院 BAND 2
港島東區 蘇浙公學 BAND 2
港島東區 嶺南衡怡紀念中學 BAND 2
港島東區 嶺南中學 BAND 2
港島東區 張振興伉儷書院 BAND 3
港島東區 閩僑中學 BAND 3
港島東區 聖公會李福慶中學 BAND 3
港島東區 聖貞德中學 BAND 3
港島東區 明愛柴灣馬登基金中學 BAND 3
港島東區 中華基督教會桂華山中學 BAND 3
港島東區 筲箕灣東官立中學 BAND 3
港島東區 炮台山循道衞理中學 -
港島東區 茵維特中學 -
灣仔區 https://www.schooland.hk/ss/wan-chai
灣仔區 皇仁書院 BAND 1
灣仔區 瑪利曼中學 BAND 1
灣仔區 香港華仁書院 BAND 1
灣仔區 聖保祿學校 BAND 1
灣仔區 香港真光中學 BAND 1
灣仔區 聖保祿中學 BAND 1
灣仔區 聖公會鄧肇堅中學 BAND 1
灣仔區 嘉諾撒聖方濟各書院 BAND 1
灣仔區 香港鄧鏡波書院 BAND 2
灣仔區 佛教黃鳳翎中學 BAND 2
灣仔區 何東中學 BAND 2
灣仔區 玫瑰崗中學 BAND 2
灣仔區 孔聖堂中學 BAND 3
灣仔區 鄧肇堅維多利亞官立中學 BAND 3
灣仔區 東華三院李潤田紀念中學 BAND 3
灣仔區 北角協同中學 BAND 3
灣仔區 中華基督教會公理高中書院 -
港島南區 https://www.schooland.hk/ss/southern
港島南區 嘉諾撒聖心書院 BAND 1
港島南區 港大同學會書院 BAND 1
港島南區 聖士提反書院 BAND 1
港島南區 香港真光書院 BAND 2
港島南區 聖公會呂明才中學 BAND 2
港島南區 香港仔浸信會呂明才書院 BAND 2
港島南區 聖伯多祿中學 BAND 2
港島南區 嘉諾撒培德書院 BAND 2
港島南區 新會商會陳白沙紀念中學 BAND 2
港島南區 余振強紀念第二中學 BAND 3
港島南區 香港仔工業學校 BAND 3
港島南區 明愛莊月明中學 BAND 3
港島南區 明愛胡振中中學 BAND 3
港島南區 香港航海學校 BAND 3
港島南區 培英中學 BAND 3
港島南區 弘立書院 -
港島南區 滬江維多利亞學校 -
港島南區 漢鼎書院 -
離島區 https://www.schooland.hk/ss/islands
離島區 保良局馬錦明夫人章馥仙中學 BAND 1
離島區 東涌天主教學校 BAND 2
離島區 港青基信書院 BAND 2
離島區 黃楚標中學 BAND 2
離島區 可譽中學 BAND 2
離島區 靈糧堂怡文中學 BAND 2
離島區 長洲官立中學 BAND 3
離島區 佛教筏可紀念中學 BAND 3
離島區 佛教慧因法師紀念中學 BAND 3
離島區 明愛華德中書院 -
離島區 智新書院 -
九龍城區 https://www.schooland.hk/ss/kowloon-city
九龍城區 華英中學 BAND 1
九龍城區 喇沙書院 BAND 1
九龍城區 協恩中學 BAND 1
九龍城區 瑪利諾修院學校 BAND 1
九龍城區 迦密中學 BAND 1
九龍城區 拔萃男書院 BAND 1
九龍城區 香港培正中學 BAND 1
九龍城區 何明華會督銀禧中學 BAND 1
九龍城區 旅港開平商會中學 BAND 1
九龍城區 九龍真光中學 BAND 1
九龍城區 民生書院 BAND 1
九龍城區 東華三院黃笏南中學 BAND 1
九龍城區 保良局顏寶鈴書院 BAND 1
九龍城區 香港培道中學 BAND 1
九龍城區 嘉諾撒聖家書院 BAND 1
九龍城區 基督教女青年會丘佐榮中學 BAND 1
九龍城區 陳瑞祺喇沙書院 BAND 2
九龍城區 何文田官立中學 BAND 2
九龍城區 九龍文理書院 BAND 2
九龍城區 聖公會聖三一堂中學 BAND 2
九龍城區 鄧鏡波學校 BAND 2
九龍城區 順德聯誼總會胡兆熾中學 BAND 2
九龍城區 創知中學 BAND 2
九龍城區 禮賢會彭學高紀念中學 BAND 2
九龍城區 九龍塘學校 BAND 2
九龍城區 中華基督教會基道中學 BAND 2
九龍城區 五旬節中學 BAND 2
九龍城區 德蘭中學 BAND 2
九龍城區 新亞中學 BAND 3
九龍城區 聖公會蔡功譜中學 BAND 3
九龍城區 獻主會聖母院書院 BAND 3
九龍城區 余振強紀念中學 BAND 3
九龍城區 賽馬會官立中學 BAND 3
九龍城區 聖公會聖匠中學 BAND 3
九龍城區 香港兆基創意書院 -
黃大仙區 https://www.schooland.hk/ss/wong-tai-sin
黃大仙區 德望學校 BAND 1
黃大仙區 保良局第一張永慶中學 BAND 1
黃大仙區 中華基督教會協和書院 BAND 1
黃大仙區 保良局何蔭棠中學 BAND 1
黃大仙區 德愛中學 BAND 1
黃大仙區 可立中學 BAND 1
黃大仙區 聖母書院 BAND 1
黃大仙區 佛教孔仙洲紀念中學 BAND 2
黃大仙區 聖文德書院 BAND 2
黃大仙區 香港神託會培敦中學 BAND 2
黃大仙區 彩虹邨天主教英文中學 BAND 2
黃大仙區 李求恩紀念中學 BAND 2
黃大仙區 天主教伍華中學 BAND 2
黃大仙區 五旬節聖潔會永光書院 BAND 2
黃大仙區 中華基督教會扶輪中學 BAND 3
黃大仙區 潔心林炳炎中學 BAND 3
黃大仙區 樂善堂余近卿中學 BAND 3
黃大仙區 聖公會聖本德中學 BAND 3
黃大仙區 樂善堂王仲銘中學 BAND 3
黃大仙區 中華基督教會基協中學 BAND 3
黃大仙區 龍翔官立中學 BAND 3
黃大仙區 救世軍卜維廉中學 BAND 3
黃大仙區 佛教志蓮中學 -
黃大仙區 國際基督教優質音樂中學暨小學 -
黃大仙區 神召會德萃書院 -
觀塘區 https://www.schooland.hk/ss/kwun-tong
觀塘區 藍田聖保祿中學 BAND 1
觀塘區 中華基督教會蒙民偉書院 BAND 1
觀塘區 觀塘官立中學 BAND 1
觀塘區 順利天主教中學 BAND 1
觀塘區 聖言中學 BAND 1
觀塘區 聖傑靈女子中學 BAND 1
觀塘區 匯基書院東九龍 BAND 1
觀塘區 福建中學 BAND 1
觀塘區 觀塘瑪利諾書院 BAND 1
觀塘區 梁式芝書院 BAND 1
觀塘區 仁濟醫院羅陳楚思中學 BAND 1
觀塘區 聖道迦南書院 BAND 2
觀塘區 寧波公學 BAND 2
觀塘區 寧波第二中學 BAND 2
觀塘區 呂郭碧鳳中學 BAND 2
觀塘區 聖安當女書院 BAND 2
觀塘區 聖若瑟英文中學 BAND 2
觀塘區 聖公會基孝中學 BAND 2
觀塘區 聖公會梁季彜中學 BAND 2
觀塘區 基督教聖約教會堅樂中學 BAND 2
觀塘區 中華基督教會基智中學 BAND 2
觀塘區 五邑司徒浩中學 BAND 2
觀塘區 高雷中學 BAND 2
觀塘區 香港聖公會何明華會督中學 BAND 3
觀塘區 地利亞修女紀念學校(協和) BAND 3
觀塘區 香港布廠商會朱石麟中學 BAND 3
觀塘區 觀塘功樂官立中學 BAND 3
觀塘區 瑪利諾中學 BAND 3
觀塘區 香港道教聯合會青松中學 BAND 3
觀塘區 佛教何南金中學 BAND 3
觀塘區 慕光英文書院 BAND 3
觀塘區 地利亞修女紀念學校(協和二中) BAND 3
觀塘區 天主教普照中學 BAND 3
觀塘區 路德會官塘書院 -
觀塘區 示昕學校 -
油尖旺區 https://www.schooland.hk/ss/yau-tsim-mong
油尖旺區 拔萃女書院 BAND 1
油尖旺區 伊利沙伯中學 BAND 1
油尖旺區 嘉諾撒聖瑪利書院 BAND 1
油尖旺區 真光女書院 BAND 1
油尖旺區 聖芳濟書院 BAND 1
油尖旺區 華仁書院(九龍) BAND 1
油尖旺區 循道中學 BAND 1
油尖旺區 中華基督教會銘基書院 BAND 1
油尖旺區 李國寶中學 BAND 1
油尖旺區 基督教香港信義會信義中學 BAND 2
油尖旺區 港九潮州公會中學 BAND 2
油尖旺區 世界龍岡學校劉皇發中學 BAND 2
油尖旺區 麗澤中學 BAND 3
油尖旺區 聖公會諸聖中學 BAND 3
油尖旺區 天主教新民書院 BAND 3
油尖旺區 九龍三育中學 BAND 3
油尖旺區 官立嘉道理爵士中學 BAND 3
油尖旺區 保良局莊啟程預科書院 -
油尖旺區 瑪利亞書院 -
深水埗區 https://www.schooland.hk/ss/sham-shui-po
深水埗區 寶血會上智英文書院 BAND 1
深水埗區 聖母玫瑰書院 BAND 1
深水埗區 中華基督教會銘賢書院 BAND 1
深水埗區 英華書院 BAND 1
深水埗區 黃棣珊紀念中學 BAND 1
深水埗區 聖瑪加利男女英文中小學 BAND 1
深水埗區 德雅中學 BAND 1
深水埗區 長沙灣天主教英文中學 BAND 1
深水埗區 香島中學 BAND 1
深水埗區 瑪利諾神父教會學校 BAND 1
深水埗區 保良局蔡繼有學校 BAND 1
深水埗區 基督教崇真中學 BAND 1
深水埗區 路德會協同中學 BAND 2
深水埗區 佛教大雄中學 BAND 2
深水埗區 東華三院張明添中學 BAND 2
深水埗區 匯基書院 BAND 2
深水埗區 保良局唐乃勤初中書院 BAND 2
深水埗區 地利亞修女紀念學校(百老匯) BAND 2
深水埗區 莫慶堯中學 BAND 2
深水埗區 陳樹渠紀念中學 BAND 3
深水埗區 德貞女子中學 BAND 3
深水埗區 九龍工業學校 BAND 3
深水埗區 中聖書院 BAND 3
深水埗區 廠商會中學 BAND 3
深水埗區 地利亞修女紀念學校(吉利徑) BAND 3
深水埗區 天主教南華中學 BAND 3
深水埗區 惠僑英文中學 BAND 3
深水埗區 崇正中學 -
葵青區 https://www.schooland.hk/ss/kwai-tsing
葵青區 中華傳道會安柱中學 BAND 1
葵青區 天主教母佑會蕭明中學 BAND 1
葵青區 聖公會林護紀念中學 BAND 1
葵青區 佛教善德英文中學 BAND 1
葵青區 保良局羅傑承(一九八三)中學 BAND 1
葵青區 保祿六世書院 BAND 1
葵青區 順德聯誼總會李兆基中學 BAND 1
葵青區 東華三院陳兆民中學 BAND 1
葵青區 中華基督教會全完中學 BAND 1
葵青區 迦密愛禮信中學 BAND 2
葵青區 東華三院伍若瑜夫人紀念中學 BAND 2
葵青區 東華三院吳祥川紀念中學 BAND 2
葵青區 荔景天主教中學 BAND 2
葵青區 中華傳道會李賢堯紀念中學 BAND 2
葵青區 葵涌蘇浙公學 BAND 2
葵青區 樂善堂顧超文中學 BAND 2
葵青區 皇仁舊生會中學 BAND 2
葵青區 石籬天主教中學 BAND 2
葵青區 中華基督教會燕京書院 BAND 2
葵青區 葵涌裘錦秋中學 BAND 2
葵青區 樂善堂梁植偉紀念中學 BAND 2
葵青區 佛教葉紀南紀念中學 BAND 3
葵青區 葵涌循道中學 BAND 3
葵青區 陳南昌紀念中學 BAND 3
葵青區 嶺南鍾榮光博士紀念中學 BAND 3
葵青區 圓玄學院第一中學 BAND 3
葵青區 獅子會中學 BAND 3
葵青區 天主教慈幼會伍少梅中學 BAND 3
葵青區 李惠利中學 BAND 3
葵青區 明愛聖若瑟中學 BAND 3
葵青區 棉紡會中學 BAND 3
荃灣區 https://www.schooland.hk/ss/tsuen-wan
荃灣區 荃灣官立中學 BAND 1
荃灣區 可風中學 BAND 1
荃灣區 何傳耀紀念中學 BAND 1
荃灣區 王少清中學 BAND 1
荃灣區 廖寶珊紀念書院 BAND 2
荃灣區 保良局李城璧中學 BAND 2
荃灣區 梁省德中學 BAND 2
荃灣區 荃灣聖芳濟中學 BAND 2
荃灣區 保良局姚連生中學 BAND 3
荃灣區 胡漢輝中學 BAND 3
荃灣區 仁濟醫院林百欣中學 BAND 3
荃灣區 路德會呂明才中學 BAND 3
荃灣區 聖公會李炳中學 BAND 3
沙田區 https://www.schooland.hk/ss/sha-tin
沙田區 沙田崇真中學 BAND 1
沙田區 浸信會呂明才中學 BAND 1
沙田區 沙田培英中學 BAND 1
沙田區 聖公會林裘謀中學 BAND 1
沙田區 聖公會曾肇添中學 BAND 1
沙田區 天主教郭得勝中學 BAND 1
沙田區 五旬節林漢光中學 BAND 1
沙田區 沙田官立中學 BAND 1
沙田區 沙田蘇浙公學 BAND 1
沙田區 王錦輝中小學 BAND 1
沙田區 培僑書院 BAND 1
沙田區 沙田循道衞理中學 BAND 1
沙田區 聖羅撒書院 BAND 1
沙田區 聖母無玷聖心書院 BAND 1
沙田區 宣道會鄭榮之中學 BAND 1
沙田區 賽馬會體藝中學 BAND 1
沙田區 香港神託會培基書院 BAND 1
沙田區 馬鞍山聖若瑟中學 BAND 2
沙田區 馬鞍山崇真中學 BAND 2
沙田區 保良局胡忠中學 BAND 2
沙田區 基督書院 BAND 2
沙田區 馮堯敬紀念中學 BAND 2
沙田區 樂善堂楊葛小琳中學 BAND 2
沙田區 青年會書院 BAND 2
沙田區 陳震夏中學 BAND 2
沙田區 博愛醫院陳楷紀念中學 BAND 2
沙田區 佛教覺光法師中學 BAND 2
沙田區 東莞工商總會劉百樂中學 BAND 2
沙田區 梁文燕紀念中學(沙田) BAND 2
沙田區 林大輝中學 BAND 2
沙田區 德信中學 BAND 2
沙田區 東華三院馮黃鳳亭中學 BAND 2
沙田區 佛教黃允畋中學 BAND 3
沙田區 五育中學 BAND 3
沙田區 台山商會中學 BAND 3
沙田區 東華三院黃鳳翎中學 BAND 3
沙田區 東華三院邱金元中學 BAND 3
沙田區 潮州會館中學 BAND 3
沙田區 保良局朱敬文中學 BAND 3
沙田區 樂道中學 BAND 3
沙田區 曾璧山(崇蘭)中學 BAND 3
沙田區 明愛馬鞍山中學 BAND 3
沙田區 仁濟醫院董之英紀念中學 BAND 3
沙田區 啓新書院 -
大埔區 https://www.schooland.hk/ss/tai-po
大埔區 迦密柏雨中學 BAND 1
大埔區 王肇枝中學 BAND 1
大埔區 聖公會莫壽增會督中學 BAND 1
大埔區 恩主教書院 BAND 1
大埔區 南亞路德會沐恩中學 BAND 1
大埔區 神召會康樂中學 BAND 2
大埔區 孔教學院大成何郭佩珍中學 BAND 2
大埔區 港九街坊婦女會孫方中書院 BAND 2
大埔區 圓玄學院第二中學 BAND 2
大埔區 救恩書院 BAND 2
大埔區 羅定邦中學 BAND 2
大埔區 迦密聖道中學 BAND 2
大埔區 大埔三育中學 BAND 3
大埔區 中華聖潔會靈風中學 BAND 3
大埔區 靈糧堂劉梅軒中學 BAND 3
大埔區 佛教大光慈航中學 BAND 3
大埔區 香港紅卍字會大埔卍慈中學 BAND 3
大埔區 香港教師會李興貴中學 BAND 3
大埔區 新界鄉議局大埔區中學 BAND 3
大埔區 馮梁結紀念中學 BAND 3
大埔區 香港墨爾文國際學校 -
大埔區 大光德萃書院 -
西貢區 https://www.schooland.hk/ss/sai-kung
西貢區 景嶺書院 BAND 1
西貢區 迦密主恩中學 BAND 1
西貢區 優才楊殷有娣書院 BAND 1
西貢區 基督教宣道會宣基中學 BAND 1
西貢區 保良局羅氏基金中學 BAND 1
西貢區 播道書院 BAND 1
西貢區 將軍澳官立中學 BAND 1
西貢區 港澳信義會慕德中學 BAND 2
西貢區 真道書院 BAND 2
西貢區 仁濟醫院王華湘中學 BAND 2
西貢區 保良局甲子何玉清中學 BAND 2
西貢區 順德聯誼總會鄭裕彤中學 BAND 2
西貢區 東華三院呂潤財紀念中學 BAND 2
西貢區 將軍澳香島中學 BAND 2
西貢區 圓玄學院第三中學 BAND 2
西貢區 寶覺中學 BAND 2
西貢區 新界西貢坑口區鄭植之中學 BAND 2
西貢區 鄧英喜中學 BAND 2
西貢區 萬鈞匯知中學 BAND 3
西貢區 天主教鳴遠中學 BAND 3
西貢區 張沛松紀念中學 BAND 3
西貢區 香海正覺蓮社佛教正覺中學 BAND 3
西貢區 馬陳端喜紀念中學 BAND 3
西貢區 西貢崇真天主教學校 BAND 3
西貢區 仁濟醫院靚次伯紀念中學 BAND 3
西貢區 啟思中學 -
西貢區 香港復臨學校 -
屯門區 https://www.schooland.hk/ss/tuen-mun
屯門區 宣道會陳瑞芝紀念中學 BAND 1
屯門區 保良局百周年李兆忠紀念中學 BAND 1
屯門區 保良局董玉娣中學 BAND 1
屯門區 順德聯誼總會梁銶琚中學 BAND 1
屯門區 順德聯誼總會譚伯羽中學 BAND 1
屯門區 馬可賓紀念中學 BAND 1
屯門區 仁愛堂田家炳中學 BAND 1
屯門區 南屯門官立中學 BAND 1
屯門區 屯門官立中學 BAND 1
屯門區 妙法寺劉金龍中學 BAND 2
屯門區 屯門天主教中學 BAND 2
屯門區 浸信會永隆中學 BAND 2
屯門區 宣道中學 BAND 2
屯門區 路德會呂祥光中學 BAND 2
屯門區 崇真書院 BAND 2
屯門區 東華三院辛亥年總理中學 BAND 2
屯門區 迦密唐賓南紀念中學 BAND 2
屯門區 香海正覺蓮社佛教梁植偉中學 BAND 2
屯門區 新生命教育協會平安福音中學 BAND 2
屯門區 中華基督教會何福堂書院 BAND 3
屯門區 屯門裘錦秋中學 BAND 3
屯門區 聖公會聖西門呂明才中學 BAND 3
屯門區 東華三院邱子田紀念中學 BAND 3
屯門區 仁濟醫院第二中學 BAND 3
屯門區 仁愛堂陳黃淑芳紀念中學 BAND 3
屯門區 譚李麗芬紀念中學 BAND 3
屯門區 青松侯寶垣中學 BAND 3
屯門區 鐘聲慈善社胡陳金枝中學 BAND 3
屯門區 可藝中學 BAND 3
屯門區 加拿大神召會嘉智中學 BAND 3
屯門區 新會商會中學 BAND 3
屯門區 深培中學 BAND 3
屯門區 佛教沈香林紀念中學 BAND 3
屯門區 明愛屯門馬登基金中學 BAND 3
屯門區 廠商會蔡章閣中學 BAND 3
屯門區 恩平工商會李琳明中學 BAND 3
屯門區 東華三院鄺錫坤伉儷中學 -
元朗區 https://www.schooland.hk/ss/yuen-long
元朗區 新界鄉議局元朗區中學 BAND 1
元朗區 天主教崇德英文書院 BAND 1
元朗區 元朗信義中學 BAND 1
元朗區 趙聿修紀念中學 BAND 1
元朗區 香港青年協會李兆基書院 BAND 1
元朗區 中華基督教會基元中學 BAND 1
元朗區 聖公會白約翰會督中學 BAND 1
元朗區 香港管理專業協會羅桂祥中學 BAND 1
元朗區 東華三院盧幹庭紀念中學 BAND 1
元朗區 元朗商會中學 BAND 1
元朗區 中華基督教會基朗中學 BAND 2
元朗區 伊利沙伯中學舊生會中學 BAND 2
元朗區 順德聯誼總會翁祐中學 BAND 2
元朗區 十八鄉鄉事委員會公益社中學 BAND 2
元朗區 中華基督教青年會中學 BAND 2
元朗區 張煊昌中學 BAND 2
元朗區 元朗裘錦秋中學 BAND 2
元朗區 博愛醫院鄧佩瓊紀念中學 BAND 2
元朗區 天水圍官立中學 BAND 2
元朗區 天水圍循道衞理中學 BAND 2
元朗區 鄧兆棠中學 BAND 2
元朗區 宏信書院 BAND 2
元朗區 元朗公立中學 BAND 2
元朗區 天水圍香島中學 BAND 3
元朗區 中華基督教會方潤華中學 BAND 3
元朗區 金巴崙長老會耀道中學 BAND 3
元朗區 路德會西門英才中學 BAND 3
元朗區 可道中學 BAND 3
元朗區 東華三院馬振玉紀念中學 BAND 3
元朗區 萬鈞伯裘書院 BAND 3
元朗區 陳呂重德紀念中學 BAND 3
元朗區 湯國華中學 BAND 3
元朗區 賽馬會萬鈞毅智書院 BAND 3
元朗區 伯特利中學 BAND 3
元朗區 佛教茂峰法師紀念中學 BAND 3
元朗區 明愛元朗陳震夏中學 BAND 3
元朗區 天主教培聖中學 BAND 3
元朗區 東華三院郭一葦中學 BAND 3
元朗區 元朗天主教中學 BAND 3
新界北區 https://www.schooland.hk/ss/north
新界北區 鄧顯紀念中學 BAND 1
新界北區 東華三院甲寅年總理中學 BAND 1
新界北區 風采中學 BAND 1
新界北區 聖公會陳融中學 BAND 1
新界北區 田家炳中學 BAND 1
新界北區 東華三院李嘉誠中學 BAND 1
新界北區 粉嶺禮賢會中學 BAND 2
新界北區 鳳溪廖萬石堂中學 BAND 2
新界北區 保良局馬錦明中學 BAND 2
新界北區 宣道會陳朱素華紀念中學 BAND 2
新界北區 粉嶺救恩書院 BAND 2
新界北區 基督教香港信義會心誠中學 BAND 2
新界北區 馬錦燦紀念英文中學 BAND 2
新界北區 鳳溪第一中學 BAND 2
新界北區 新界喇沙中學 BAND 3
新界北區 聖芳濟各書院 BAND 3
新界北區 明愛粉嶺陳震夏中學 BAND 3
新界北區 中華基督教會基新中學 BAND 3
新界北區 粉嶺官立中學 BAND 3
新界北區 上水官立中學 BAND 3
'''
