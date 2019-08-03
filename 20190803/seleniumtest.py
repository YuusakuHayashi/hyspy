from hys import hysseleniumer
from hys import hysfiler

entry_url = "https://trello.com/login";
config = "cfg.txt"

sel = hysseleniumer.HysSeleniumer(entry_url)
fil = hysfiler.HysFiler(config)

cfg = fil.read_user_cfg()

ui = sel.wait_by_id("user");
ui.send_keys(cfg["email"]);

#ui = wait_by_id("password");
#ui.send_keys("********");

ui = sel.wait_by_id("login");
ui.click();

print(sel.__ex_path)

#driver.get(next_url);

#ui = wait_by_xpath("//*[@id='board']/div[1]/div/div[2]/a[1]");
#ui.click();
#
#ui = wait_by_class_name("mod-card-back-title js-card-detail-title-input");
#ui.click();
