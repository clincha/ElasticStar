# Business Dashboard

I rent my flat out on AirBnb and all the revenue and expenditure passes through a Starling business account. When I began this project I didn't expect that I would ever have a flat I rented out. Once I started spending and receiving money for the flat I wanted a good way to visualise the data. Starling have some good tools for that but using Elastic I have a lot more flexibility with the way I choose to display it. Here is a picture of my main dashboard:

![business-dashboards-01.png](/images/business-dashboard-01.png)

I use the graph on the left to give me a quick understanding of revenue vs expenditure. The right hand side pie graph lets me understand how my income and expenditure breaks down. This is especially useful for me to see where the majority of my expenses are. Using that information I can focus on reducing the expenses to maximise profit. Having Elasticsearch and Kibana as the engine and visualiser allows me to interact with the data in ways I wouldn't be able to do with other tools. For example, by filtering down on the direction of the cash flow I can quickly dig down into expenses and get a more detailed view:

![business-dashboard-02.png](/images/business-dashboard-02.png)
