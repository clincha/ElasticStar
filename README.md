[![Populate Elastic Cloud](https://github.com/clincha/StarSheet/actions/workflows/populate-personal-accounts.yml/badge.svg)](https://github.com/clincha/StarSheet/actions/workflows/populate-elastic-cloud.yml)

# Project Report: Financial Data Management and Visualization

## Introduction:

In 2018, I discovered Starling Bank while residing and working in London. Being a programmer, I was intrigued by the bank's API capabilities and thought it would make a fascinating foundation for various projects. I began using the card for all my transactions to keep track of my spending and make budgeting easier. This project was born out of that idea and is called "Star Sheet".

## Phase 1: Data Collection and Processing

I started by extracting all data from Starling Bank statements and pumping it into a budgeting spreadsheet. The statements API returns a list of statements in either CSV or PDF format. I chose the CSV format, removed the header, and parsed the remaining lines for their data. This process was repeated for each statement, providing me with a rudimentary list of the most important data fields.

## Phase 2: Data Storage and Visualization

I then looked into the Google Sheets API and used it to replace a target spreadsheet with the data collected from Starling Bank. The API was also used to format the spreadsheet and save the data. I scheduled the program to run every hour using GitHub Actions, which met my needs for tracking my spending and budgeting. However, as time passed, I noticed that the amount of effort required to create new visualizations became increasingly painful. This led me to believe that Google Sheets was not the final solution to the problem.

With the limitations of the first system clear, I created a set of user stories to help inform the next iteration of the project.

### User stories for improvement

As a recruiter, I want to know what a candidate is capable of, so that I can recruit them into the correct role.

As a Starling Bank account holder, I want to make custom visualizations for my bank account, so that I can quickly ascertain financial information that is relevant to me.

As a Starling Bank account holder, I want to explore every piece of data that Starling has, so that I can build a holistic view of my opening.

As a Starling Bank account holder with multiple accounts, I want to be able to see the data from all the accounts, so that I can explore trends from each account and between the accounts.

As a saver, I want to rapidly build and destroy visualizations, so that I can keep my view as relevant as possible.

### Elastic Stack

To overcome the limitations encountered in Phase 2, I decided to use the Elastic Stack as the repository and visualization tool for the next iteration. The Elastic Stack is a powerful combination of tools that includes Elasticsearch, Logstash, and Kibana. It offers a flexible and scalable platform for managing large amounts of data and provides a user-friendly interface for data visualization.

## Phase 3: Elasticity

I have successfully completed the next stage of my personal project. My main objective for this stage was to find a more effective and efficient solution for storing and visualizing my financial data. After exploring my options, I decided to use Elastic Stack as the repository and visualization tool for the project.

To achieve this, I first provisioned an Elastic Stack instance on Elastic cloud. Then I changed the code to be able to handle multiple account types, and created a project readme to explain the application to potential recruiters.

The visualizations were a critical aspect of this project. I created a dashboard in Kibana to display several key metrics such as total spend per category, spending over time per category, total spending per month, total outgoing and incoming for each account, mortgage spending, and a map of where money was being spent. By using Kibana, I was able to create interactive and dynamic visualizations that made it easy to identify patterns and trends in my spending.

In addition to improving the visualizations, I also improved the performance of the solution by implementing caching and using the bulk API for Elastic Stack. This reduced the time taken for the solution to run from a couple of minutes to less than 10 seconds. Finally, I improved the data from Starling by changing to the feed API instead of the statement API. This provided a wealth of additional information such as location data for transactions, unique identifiers, currency data, and the status and type of transactions.

## Conclusion:

In conclusion, the use of Elastic Stack has allowed me to store and visualize my financial data in a more effective and efficient manner. The improved performance and additional data have made it easier to track and understand my spending, and the interactive visualizations have provided valuable insights into my financial habits. Overall, I am satisfied with the results of this stage of the project and am excited to continue improving it in the future.