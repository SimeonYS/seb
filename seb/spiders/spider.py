import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SebItem
from itemloaders.processors import TakeFirst
import json
import requests
import datetime
from scrapy import Selector

pattern = r'(\xa0)?'

url = "https://www.seb.ee/views/ajax?field_news_category_tid[0]=288&field_news_category_tid[1]=273&field_news_category_tid[2]=274&field_news_category_tid[3]=277"

payload="field_news_category_tid%5B%5D=288&field_news_category_tid%5B%5D=273&field_news_category_tid%5B%5D=274&field_news_category_tid%5B%5D=277&date_filter%5Bvalue%5D%5Byear%5D={}&date_filter%5Bvalue%5D%5Bmonth%5D=0&view_name=news_archive&view_display_id=page&view_args=&view_path=news&view_base_path=news&view_dom_id=ca11d1b2552d574b44c44582b20ac081&pager_element=0&ajax_html_ids%5B%5D=www-widgetapi-script&ajax_html_ids%5B%5D=skip-link&ajax_html_ids%5B%5D=box00&ajax_html_ids%5B%5D=box01&ajax_html_ids%5B%5D=box02&ajax_html_ids%5B%5D=header01&ajax_html_ids%5B%5D=header02&ajax_html_ids%5B%5D=logo&ajax_html_ids%5B%5D=box03&ajax_html_ids%5B%5D=menu01&ajax_html_ids%5B%5D=block-block-2&ajax_html_ids%5B%5D=profile01&ajax_html_ids%5B%5D=profile01&ajax_html_ids%5B%5D=seb-search-form&ajax_html_ids%5B%5D=edit-container&ajax_html_ids%5B%5D=searchid01&ajax_html_ids%5B%5D=edit-submit&ajax_html_ids%5B%5D=profile01drop&ajax_html_ids%5B%5D=block-seb-headertabs&ajax_html_ids%5B%5D=block-seb-dropdown-menu&ajax_html_ids%5B%5D=box04&ajax_html_ids%5B%5D=content01&ajax_html_ids%5B%5D=page-title&ajax_html_ids%5B%5D=block-system-main&ajax_html_ids%5B%5D=views-exposed-form-news-archive-page&ajax_html_ids%5B%5D=edit-field-news-category-tid--14-wrapper&ajax_html_ids%5B%5D=edit-field-news-category-tid--14&ajax_html_ids%5B%5D=edit-date-filter-wrapper&ajax_html_ids%5B%5D=edit-date-filter-value-wrapper&ajax_html_ids%5B%5D=edit-date-filter-value-inside-wrapper&ajax_html_ids%5B%5D=edit-date-filter-value--14&ajax_html_ids%5B%5D=edit-date-filter-value-year--14&ajax_html_ids%5B%5D=edit-date-filter-value-month--14&ajax_html_ids%5B%5D=edit-submit-news-archive--14&ajax_html_ids%5B%5D=block-block-11&ajax_html_ids%5B%5D=block-block-6&ajax_html_ids%5B%5D=hiddencontent&ajax_html_ids%5B%5D=contact-us-ee&ajax_html_ids%5B%5D=block-block-347&ajax_html_ids%5B%5D=seb-bot-window&ajax_html_ids%5B%5D=block-block-3&ajax_html_ids%5B%5D=block-seb-breadcrumb&ajax_html_ids%5B%5D=block-seb-footermenu&ajax_html_ids%5B%5D=block-block-4&ajax_html_ids%5B%5D=notsupported&ajax_html_ids%5B%5D=logo-min&ajax_html_ids%5B%5D=tooltip&ajax_html_ids%5B%5D=tooltip-inner&ajax_html_ids%5B%5D=tooltip-arrow&ajax_html_ids%5B%5D=ui-id-1&ajax_page_state%5Btheme%5D=seb_theme&ajax_page_state%5Btheme_token%5D=2Xe1rQi--dxfem4fiDaTao_szKsh9Uvx8_ErUg0KmzE&ajax_page_state%5Bcss%5D%5B0%5D=1&ajax_page_state%5Bcss%5D%5B1%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.base.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.menus.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.messages.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fcck_multiple_field_remove%2Fcss%2Fcck_multiple_field_remove.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_api%2Fdate.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fdate%2Fdate_popup%2Fthemes%2Fdatepicker.1.7.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Ffield%2Ftheme%2Ffield.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fnode%2Fnode.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fuser%2Fuser.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fcss%2Fviews.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Fmtp%2Fstyle.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Fadd_design.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Fcredit_products_custom.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Fcustom0.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Ffix_cookie.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Ffix_design.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2FfundChooserFix.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Fkampaaniad.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Fbot.css%5D=1&ajax_page_state%5Bcss%5D%5Bpublic%3A%2F%2Fweb%2Fcss%2Fgenesysfix.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fckeditor%2Fcss%2Fckeditor.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fctools%2Fcss%2Fctools.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Flocale%2Flocale.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Ffonts%2Ffonts.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_notsupported.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_frame_narrow.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_frame_narrow_extend.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_content_portable.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_content_desktop.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_custom_content_desktop.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_frame_medium.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_frame_wide.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_print.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fstyles_custom.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fcss%2Fseb_custom_print.css%5D=1&ajax_page_state%5Bjs%5D%5B0%5D=1&ajax_page_state%5Bjs%5D%5B1%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fjquery_update%2Freplace%2Fjquery%2F1.10%2Fjquery.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery-extend-3.4.0.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery-html-prefilter-3.5.0-backport.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery.once.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fdrupal.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fjquery_update%2Freplace%2Fmisc%2Fjquery.form.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fajax.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fjquery_update%2Fjs%2Fjquery_update.js%5D=1&ajax_page_state%5Bjs%5D%5Bpublic%3A%2F%2Fweb%2Fjs%2Fadobe%2FsatelliteLib-verification.js%5D=1&ajax_page_state%5Bjs%5D%5Bpublic%3A%2F%2Fweb%2Fjs%2Funetisisenemine.2.js%5D=1&ajax_page_state%5Bjs%5D%5Bpublic%3A%2F%2Fweb%2Fjs%2Fcookiefix.js%5D=1&ajax_page_state%5Bjs%5D%5Bpublic%3A%2F%2Flanguages%2Fet_5lmafuc25jiK6NXIHbnnjfxOFK7lYJvAykFcNgWZiPU.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fseb%2Fjs%2Fjquery.cookie.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fseb%2Fjs%2Fcheck_language.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fctools%2Fjs%2Fauto-submit.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fjs%2Fbase.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fprogress.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fcontrib%2Fviews%2Fjs%2Fajax_view.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fjquery.browser.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fbootstrap.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fbootstrap.multiselect.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fjquery.responsiveiframe.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fjquery.ui.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fjquery.cookie.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fjquery.tablesorter.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fjquery.extensions.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fcookie-consent.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fporthole.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fipadlabels.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fscripts.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fseb_theme%2Fjs%2Fseb_custom.js%5D=1&ajax_page_state%5Bjquery_version%5D=1.10"
headers = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'https://www.seb.ee',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.seb.ee/uudiste-arhiiv?field_news_category_tid[0]=288&field_news_category_tid[1]=273&field_news_category_tid[2]=274&field_news_category_tid[3]=277',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cookie': 'has_js=1; responsive=default; seblanguage=et; sebsession=et; SEBConsents=%7B%22version%22%3A1%2C%22consents%22%3A%7B%22mandatory%22%3Atrue%2C%22statistical%22%3Atrue%2C%22simplified_login%22%3Atrue%7D%7D; s_fid=49500DFBDB6D8C20-176FB469B209B668; s_cc=true; s_vi=[CS]v1|302515221606B247-4000162AA3583D07[CE]; gpv_pn=www.seb.ee%7Cuudiste-arhiiv; gpv_pu=https%3A%2F%2Fwww.seb.ee%2Fuudiste-arhiiv%3Ffield_news_category_tid%255B0%255D%3D288%26field_news_category_tid%255B1%255D%3D273%26field_news_category_tid%255B2%255D%3D274%26field_news_category_tid%255B3%255D%3D277; s_sq=assebeeprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dwww.seb.ee%25257Cuudiste-arhiiv%2526link%253D{}%2526region%253Dedit-date-filter-value--14%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dwww.seb.ee%25257Cuudiste-arhiiv%2526pidt%253D1%2526oid%253Djavascript%25253Avoid%2525280%252529%25253B%2526ot%253DA'
}



class SebSpider(scrapy.Spider):
        name = 'seb'
        now = datetime.datetime.now()
        year = now.year
        start_urls = ["https://www.seb.ee/views/ajax?field_news_category_tid[0]=288&field_news_category_tid[1]=273&field_news_category_tid[2]=274&field_news_category_tid[3]=277"]


        def parse(self, response):
            data = requests.request("POST", url, headers=headers, data=payload.format(self.year))
            data = json.loads(data.text)
            container = data[2]['data']
            posts = Selector(text=container).xpath('//tr')
            for post in posts:
                date = post.xpath('.//span[@class="date-display-single"]/text()').get()
                link = post.xpath('.//a/@href').get()

                yield response.follow(link,self.parse_post,cb_kwargs=dict(date=date))

            if self.year >= 2006:
                self.year -= 1
                yield response.follow(response.url, self.parse, dont_filter=True)


        def parse_post(self, response,date):
            title = response.xpath('//h1/text()').get()
            content = response.xpath('//div[@class="field-item even"]//text()[not (ancestor::script)]').getall()
            content = [p.strip() for p in content if p.strip()]
            content = re.sub(pattern, "",' '.join(content))

            item = ItemLoader(item=SebItem(), response=response)
            item.default_output_processor = TakeFirst()

            item.add_value('title', title)
            item.add_value('link', response.url)
            item.add_value('content', content)
            item.add_value('date', date)

            yield item.load_item()
