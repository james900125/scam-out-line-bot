# scam-out-line-bot
Line bot for Open Data Contest

需要把'YOUR_CHANNEL_ACCESS_TOKEN'和'YOUR_CHANNEL_SECRET'換成自己Linebot的

這Linebot是佈署在Heroku上執行，要更改程式的話要先安裝Heroku CLI，連結如下：
https://devcenter.heroku.com/articles/heroku-cli#download-and-install

使用命令提示字元，Heroku CLI操作如下：

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

$ heroku login

Clone the repository

Use Git to clone scam-out-line-bot's source code to your local machine.

$ heroku git:clone -a scam-out-line-bot

$ cd scam-out-line-bot


Deploy your changes


Make some changes to the code you just cloned and deploy them to Heroku using Git.

$ git add .

$ git commit -am "make it better"

$ git push heroku master
