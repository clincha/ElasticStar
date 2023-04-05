# Business Dashboard

I rent my flat out on AirBnb and all the revenue and expenditure passes through a Starling business account. When I began this project I didn't expect that I would ever have a flat I rented out. Once I started spending and receiving money for the flat I wanted a good way to visualise the data. Starling have some good tools for that but using Elastic I have a lot more flexibility with the way I choose to display it. Here is a picture of my main dashboard:

![business-dashboards-01.png](/images/business-dashboard-01.png)

I use the graph on the left to give me a quick understanding of revenue vs expenditure. The right hand side pie graph lets me understand how my income and expenditure breaks down. This is especially useful for me to see where the majority of my expenses are. Using that information I can focus on reducing the expenses to maximise profit. Having Elasticsearch and Kibana as the engine and visualiser allows me to interact with the data in ways I wouldn't be able to do with other tools. For example, by filtering down on the direction of the cash flow I can quickly dig down into expenses and get a more detailed view:

![business-dashboard-02.png](/images/business-dashboard-02.png)

The discover section in Kibana gives me the ability to quickly create new visualisations, but it also gives me the ability to dig into patterns and trends. Let's look at the cost of cleaning as an example. The first thing I do it go to the discover tool and set some of the main filtering criteria. In this case, I only want to see data from the 'clincha_starling_business' index. This will restrict data to only that account. I've only ever used one cleaner (Mary) so I can filter down to only show me those transactions.

![business-dashboard-03.png](/images/business-dashboard-03.png)

This view is already really useful. I can see all the transactions in a list and the transactions as a function of time. August is Fringe season in Edinburgh, and it's also when I first started renting out the flat. At that time the listing was optimised for shorter stays and the cleaning fees for the month reflect that. Afterward, we had a long booking with a big clean in December and another group of shorter lets.

There are also a couple of different transaction types. These reflect the cost of the clean and the cost of supplies Mary needs to clean the flat. We've only recently asked her to buy supplies instead of providing them for her so there's only one transaction marked EQUIPMENT. Later down the track it might be interesting to see this data to budget out the cost of supplies over the month/year.

While this data is interesting, I'd like to compare it to the revenue earned so that I can see the difference in cost between short term lets and longer term stays. To do this I'll save this view and then create a visualisation with the revenue data as another layer. From my other graphs I've noticed that my mortgage is my biggest other expense, so I'll add this to the visualisation as well.

![business-dashboard-04.png](/images/business-dashboard-04.png)

That's the visualisation complete. There's probably more data to add to it but for now I'm happy. I'll add it in to the main dashboard and see how it fits.

![business-dashboard-05.png](/images/business-dashboard-05.png)

I'm really happy with the result. My girlfriends first comment when I showed her was "Oh it looks like [Arthur's Seat](https://www.flickr.com/photos/hagdorned/46615646372/)". What higher praise is there? For myself, the best things about this tool are:

1. The data will automatically refresh so it's always up-to-date
2. It took me less than an hour to go from the first to the last picture. (I was writing this at the same time)
3. It helps me answer the questions I have about the transactions I make... and prompts a boatload more.

Here's hoping in a couple of years it's looking a bit more like the soaring peak of Everest.
