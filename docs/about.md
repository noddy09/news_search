## Required services:
- Searching of news with the given keyword.
- Autocomplete suggestion.
- Authentication and authorization service

## Workflow:
Get keyword requests, find results for keywords in your database.
- Create an account for using the service
- Login 
  -> Authenticate and Generate authorization token.
  -> Create WebSocket connection.
- Request with keyword
  -> Suggestion for keyword (auto-complete) from the keywords which are already available with the database.
- If News articles are found in the database:
  -> return Results
- else:
  -> Hook async task creation (celery) to fetch news from newsapi.org with the given keyword.
      -->> consume API of newsapi.org and request with the keyword.
      -->> save all articles along with keywords found.
  -> return http_202 with task id and let client subscribe for a specified task
  -> return Results when task id status changes to success/failure.

## Database:
I really wanted to use a text-based/ NoSQL / document-based database here, but due to lack of leisure and less hands-on practise with those; I'm choosing here RDBMS. Database for core business login will have 3 tables. Source, Keyword, Article.
I choose here to keep source and keywords as separate tables from a news article.

- Source: 
It is denoted to the source of the article, from which company/ organization/ institute/ magazine service has published this article.
The possibilities of getting repeated source names in articles are extremely high, so rather than adding a varchar-based column with a repeated data.

- Keyword:
Unlike source, a keyword may not be that high repeated entity. but we can indirectly force end-user to use keywords that we already cache/saved in our database by giving suggestions. 😛 So that misspelled will not create unnecessary another fetching async task. Also, keywords can be used as indexed of our articles also. we can quickly retrieve articles from our database with help of many-to-many relationships with keywords. For now, to avoid duplicate entries of the same keywords. The text which is going to be saved in the database is cleaned with the UPPER case function and with a unique key.

- Article:
Finally, all details of our news will be stored in this database. Initially, I tried to make most of the columns unique=true, and null=false. but the catch was, news provider itself sending me null values for few things. 😅 so had to revert back those columns.