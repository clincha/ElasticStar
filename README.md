[![Provision Elastic Cloud deployment](https://github.com/clincha/ElasticStar/actions/workflows/provision-elastic-deployment.yml/badge.svg?branch=master)](https://github.com/clincha/ElasticStar/actions/workflows/provision-elastic-deployment.yml)
[![Populate elastic](https://github.com/clincha/ElasticStar/actions/workflows/populate-elastic.yml/badge.svg)](https://github.com/clincha/ElasticStar/actions/workflows/populate-elastic.yml)  

[![Populate spreadsheet](https://github.com/clincha/ElasticStar/actions/workflows/populate-spreadsheet.yml/badge.svg)](https://github.com/clincha/ElasticStar/actions/workflows/populate-spreadsheet.yml)

# ElasticStar

This is a project I created to better visualise my bank transaction data. I'm using both the Elastic Stack and Google Sheets to accomplish this. Take a look at the "Documentation" folder for a deeper dive into the project or the "images" folder to see the results for yourself.

The idea is to be able to interact with my bank transaction data in a way that is more meaningful to me. I want to be able to do that in a visual way and also be able to get exact figures when I need them. I've created a dashboard using Kibana and a Google Sheet to help me do that.

There's a detailed Project Report in the "Documentation" folder along with a writeup for my AirBnb transactions dashboard. The "Issues" tab has a list of tasks left for me to do before I can call this project a wrap. There are instructions for forking the project in the "Documentation" folder if you want to make your own version (see below).

## Business Dashboard

![business-dashboard-05.png](/images/business-dashboard-05.png)

## Transport costs (2018 - 2024)

This was useful for deciding to switch to a car club instead of owning a car. I've switched now, in a year's time I'll take a look at the data again. The spikes in the graph show insurance, services and repairs. Looking at this I expect the car club costs to be lower for the number of trips I make.

![transport costs.png](/images/transport-costs.png)

## Spreadsheet output example

### Transaction feed

| Currency | Amount | Source Currency | Source Amount | Direction | Transaction Time         | Source              | Status  | Counter Party Type | Counter Party Name   | Reference                                                    | Country | Spending Category | Has Attachment | Has Receipt |
|----------|--------|-----------------|---------------|-----------|--------------------------|---------------------|---------|--------------------|----------------------|--------------------------------------------------------------|---------|-------------------|----------------|-------------|
| GBP      | 0.01   | GBP             | 0.01          | IN        | 2018-11-12T20:33:21.000Z | FASTER_PAYMENTS_IN  | SETTLED | SENDER             | PAYPAL CODE 4269     | PAYPAL CODE 4269                                             | GB      | INCOME            | FALSE          | FALSE       |
| GBP      | 8.49   | GBP             | 8.49          | OUT       | 2018-11-14T12:33:57.685Z | MASTER_CARD         | SETTLED | MERCHANT           | Pizza Hut 228        | PIZZA HUT 228          LONDON        GBR                     | GB      | EATING_OUT        | FALSE          | FALSE       |
| GBP      | 1      | GBP             | 1             | OUT       | 2018-11-15T20:53:57.620Z | MASTER_CARD         | SETTLED | MERCHANT           | Morrisons            | W M MORRISONS PLC      LONDON        GBR                     | GB      | GROCERIES         | FALSE          | FALSE       |
| GBP      | 6.8    | GBP             | 6.8           | OUT       | 2018-11-15T07:26:57.992Z | MASTER_CARD         | SETTLED | MERCHANT           | TfL                  | TfL Travel Charge      TFL.gov.uk/CP GBR                     | GB      | TRANSPORT         | FALSE          | FALSE       |
| GBP      | 9      | GBP             | 9             | OUT       | 2018-11-16T12:21:43.580Z | MASTER_CARD         | SETTLED | MERCHANT           | Old Chang Kee        | OLD CHANG KEE          LONDON  WC2N  GBR                     | GB      | EATING_OUT        | FALSE          | FALSE       |
| GBP      | 6.8    | GBP             | 6.8           | OUT       | 2018-11-19T06:44:06.740Z | MASTER_CARD         | SETTLED | MERCHANT           | TfL                  | TFL TRAVEL CH\VICTORIA STREET\TFL.GOV.UK/CP\SW1H 0TL     GBR | GB      | TRANSPORT         | FALSE          | FALSE       |
| GBP      | 0.75   | GBP             | 0.75          | OUT       | 2018-11-19T17:16:15.271Z | MASTER_CARD         | SETTLED | MERCHANT           | Sainsburys Stratford | SAINSBURYS SACAT 0002  STRATFORD     GBR                     | GB      | GROCERIES         | FALSE          | FALSE       |
| GBP      | 6.8    | GBP             | 6.8           | OUT       | 2018-11-20T03:47:08.686Z | MASTER_CARD         | SETTLED | MERCHANT           | TfL                  | TfL Travel Charge      TFL.gov.uk/CP GBR                     | GB      | TRANSPORT         | FALSE          | FALSE       |
| GBP      | 6.8    | GBP             | 6.8           | OUT       | 2018-11-22T12:06:57.222Z | MASTER_CARD         | SETTLED | MERCHANT           | TfL                  | TFL TRAVEL CH\VICTORIA STREET\TFL.GOV.UK/CP\SW1H 0TL     GBR | GB      | TRANSPORT         | FALSE          | FALSE       |
| GBP      | 7.47   | GBP             | 7.47          | OUT       | 2018-11-21T12:11:42.939Z | MASTER_CARD         | SETTLED | MERCHANT           | McDonald's           | MCDONALDS              LONDON        GBR                     | GB      | EATING_OUT        | FALSE          | FALSE       |
| GBP      | 1.4    | GBP             | 1.4           | OUT       | 2018-11-22T12:55:34.998Z | MASTER_CARD         | SETTLED | MERCHANT           | Co-op Food           | CO-OP GROUP FOOD RETAI FOREST GATE   GBR                     | GB      | GROCERIES         | FALSE          | FALSE       |
| GBP      | 11.82  | GBP             | 11.82         | OUT       | 2018-11-22T16:08:09.252Z | MASTER_CARD         | SETTLED | MERCHANT           | Kfc - Forest Gate    | KFC - FOREST GATE      LONDON        GBR                     | GB      | EATING_OUT        | FALSE          | FALSE       |
| GBP      | 12.95  | GBP             | 12.95         | OUT       | 2018-11-23T12:12:51.798Z | MASTER_CARD         | SETTLED | MERCHANT           | Nandos Covent Garden | NANDOS COVENT GARDEN   LONDON        GBR                     | GB      | EATING_OUT        | FALSE          | FALSE       |
| GBP      | 5.3    | GBP             | 5.3           | OUT       | 2018-11-26T06:55:11.603Z | MASTER_CARD         | SETTLED | MERCHANT           | TfL                  | TFL TRAVEL CH\VICTORIA STREET\TFL.GOV.UK/CP\SW1H 0TL     GBR | GB      | TRANSPORT         | FALSE          | FALSE       |
| GBP      | 5.7    | GBP             | 5.7           | OUT       | 2018-11-23T21:20:21.256Z | MASTER_CARD         | SETTLED | MERCHANT           | White Lion Antiques  | WHITE LION             LONDON        GBR                     | GB      | SHOPPING          | FALSE          | FALSE       |
| GBP      | 5.15   | GBP             | 5.15          | OUT       | 2018-11-23T21:44:04.550Z | MASTER_CARD         | SETTLED | MERCHANT           | White Lion Antiques  | WHITE LION             LONDON        GBR                     | GB      | SHOPPING          | FALSE          | FALSE       |
| GBP      | 9.5    | GBP             | 9.5           | OUT       | 2018-11-23T22:29:55.185Z | MASTER_CARD         | SETTLED | MERCHANT           | White Lion Antiques  | WHITE LION             LONDON        GBR                     | GB      | SHOPPING          | FALSE          | FALSE       |
| GBP      | 1.5    | GBP             | 1.5           | OUT       | 2018-11-26T02:38:05.046Z | MASTER_CARD         | SETTLED | MERCHANT           | TfL                  | TfL Travel Charge      TFL.gov.uk/CP GBR                     | GB      | TRANSPORT         | FALSE          | FALSE       |


### Savings spaces

| Space             | Target Currency | Target | Total Saved Currency | Total Saved | Saved Percentage | State  |
|-------------------|-----------------|--------|----------------------|-------------|------------------|--------|
| Pennies to Pounds | GBP             | 500    | GBP                  | 296.5       | 59               | ACTIVE |
| Life              | GBP             | 5000   | GBP                  | 0           | 0                | ACTIVE |


## Make your own

I wanted to have this be a website where you could press a button and make your own deployment. However, access to any kind of banking data is heavily regulated (for good reason) and going through that process would be a lot for this small application. You can still make your own version of this, but it isn't as simple as clicking a button. I've written a ([forking-instructions.md](/Documentation/forking-instructions.md)) guide which will help you through the process. If you have any issues with it please raise an issue, and I'll take a look.