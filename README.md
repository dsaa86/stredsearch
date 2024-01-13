# StredSearch

## PROJECT FILES CAN BE LOCATED IN THE 'STREDSEARCH' DIRECTORY, PREDOMINANTLY WITHIN THE 'SEARCH' APP OF DJANGO
## POSSIBLE ENHANCEMENTS AND BUGS CAN BE LOCATED UNDER 'ISSUES'

## A Unified Search Interface for StackOverflow and Reddit

StredSearch is a web application developed using Django and Django Restframework, aimed at facilitating simultaneous searches on StackOverflow and Reddit. This project showcases Python web development skills and backend technologies.

### Primary Features

* **Dual-Platform Search**: Perform searches on StackOverflow and Reddit at the same time, aggregating a broad spectrum of discussions and solutions.
  
* **Results Caching**: Implements caching of search results in a local database to improve retrieval speed for repeated queries and reduce external API calls.
  
* **API Integration**: Efficiently integrates with the APIs of StackOverflow and Reddit, highlighting the ability to work with external data sources and manage API communications.

### Purpose

StredSearch is designed to:
* Offer a convenient tool for developers and tech enthusiasts, consolidating information from key online communities.
* Be extensible such that the back-end service could be used for multiple client use-cases or platforms.
* Serve as a showcase portfolio project, demonstrating proficiency in Django-based development with a focus on API interaction, database management, and user-friendly interface design.

---

## Technical Documentation

### Frameworks & Technologies Used

* **Primary Frameworks**: Django (ver 4.2.), Django Rest Framework (ver 3.14.0)
* **Python Libraries**: See [requirements.txt](https://github.com/dsaa86/stredsearch/blob/master/stredsearch/requirements.txt) for a complete list of libraries used in this project.
* **Redis Server**: An asynchronous work queue is utilised to cache search data to a local db. Redis allows data to be cached in RAM temporarily until the appropriate queue job is actioned.
* **RQ Worker**: As this is a simple implementation of an async queue, the Django RQ framework is utilised. More complex, or production environments, would be better suited to use Celery.

### External APIs

* **StackOverflow API**: Implementation in [stackquery.py](https://github.com/dsaa86/stredsearch/blob/master/stredsearch/search/stackquery.py); data is ingested as JSON objects and assimilated to the project in a 'typical' RESTful process.
* **Reddit API**: Implementation in [redditquery.py](https://github.com/dsaa86/stredsearch/blob/master/stredsearch/search/redditquery.py); to broaden the skillset demonstrated in this project, the Reddit dataset is accessed via a typical HTTP request and the contents of the resulting page is scraped, transformed, and then ingested.
  * The contents of a Reddit page are dynamically loaded after the initial HTML has been rendered to the screen; this limits the functionality of a typical scrape.
  * A headless instance of Selenium is used to allow the dynamic HTML to render before passing this to Beautiful Soup for parsing.

### Database Schema

* [Database Schema ERD](https://github.com/dsaa86/stredsearch/blob/master/StredSearchSchema.png)
* The database is deployed using the Postgresql platform
  * This platform offers the best compromise between ease of implementation and scalability.
  * In real terms, a production version of this tool is unlikely to gather a userbase great enough to warrant a more complex database implementation. Should this need arise, there are other aspects of the codebase that could be optimised before refactoring the database technology.

### Application Architecture

* **Components**:
  
  * **Models**
    
    * Stack Params
      * *Description:* The possible parameters for a SO question, such as title and whether the question has been accepted.
      * *Extends:* models.Model
    * Stack Sort Methods
      * *Description:* The possible methods for sorting results when making a request to the SO API, such as by total votes, recent, or popular
      * *Extends:* models.Model
    * Stack Order Methods
      * *Description:* The possible methods for ordering results when making a request to the SO API, such as ascending or descending order
      * *Extends:* models.Model
    * Stack Filters
      * *Description:* Fields that allow calls to the SO API to have filtered results, for example the max and min date range that questions have been asked, or the page number of results that should be returned.
      * *Extends:* models.Model
    * Stack Question Data Fields
      * *Description:* The data fields from a SO question that we wish to store in the DB; this differs from Stack Parameters as params indicate all of the possible data that can be retrieved, whereas Data Fields indicate the data that we actually want to store.
      * *Extends:* models.Model
    * Stack Route
      * *Description:* Defines the API routing that an SO call can take, including which params are valid for a given search type.
      * *Extends:* models.Model
    * Stacak Route Meta
      * *Description:* Defines the root of the URL for an SO API call, plus any additional standard content - such as the API version number
      * *Extends:* models.Model
    * Stack User
      * *Description:* Defines a SO account attributed to a user who has created one (or more) of the questions ingested by the system
      * *Extends:* models.Model
    * Stacak Tags
      * *Description:* Defines a collection of tags that questions are assigned to in order to aid search
      * *Extends:* models.Model
    * Search Terms
      * *Description:* Defines the complete set of terms entered by a user in to the StredSearch platform for either a SO or Reddit search
      * *Extends:* models.Model
    * StredSearchQuestion
      * *Description:* Defines the outline data fields that are common to both Reddit and SO questions that are ingested via the APIs
      * *Extends:* models.Model
    * Stack Question
      * *Description:* Defines the additional question fields that are unique to a SO question
      * *Extends:* StredSearchQuestion
    * Reddit Search Type
      * *Description:* Defines whether a reddit search is looking for posts, comments, or subreddits as the return type of a query
      * *Extends:* models.Model
    * Reddit Subreddit
      * *Description:* Defines the list of subreddits that have previously been searched via the Reddit API
      * *Extends:* models.Model
    * Reddit Question
      * *Description:* Defines fields that are unique to a Reddit question
      * *Extends:* StredSearchQuestion
    * User Search Responses
      * *Description:* When a user performs a local search (via the cached results in the DB), their search term and all of the answers returned as a part of that search are stored using this model
      * *Extends:* models.Model
     
  * **API End Points**
  
    * *Stack Overflow Routes*

      * stack/get/question_by_tag/\<str:page\>/\<str:pagesize\>/\<str:fromdate\>/\<str:todate\>/\<str:order\>/\<str:sort\>/\<str:tags\>/\<str:token\>/
        * Searches SO for questions defined by a tag(s). Tags are submitted as a comma delimited string

      * stack/get/related_questions/\<str:page\>/\<str:pagesize\>/\<str:fromdate\>/\<str:todate\>/\<str:order\>/\<str:sort\>/\<str:ids\>/\<str:token\>/
        * Searches SO for questions related to a particular question(s). Questions are identified by their unique IDs.

      * stack/get/simple_search/\<str:page\>/\<str:pagesize\>/\<str:fromdate\>/\<str:todate\>/\<str:order\>/\<str:sort\>/\<str:nottagged\>/\<str:tagged\>/\<str:intitle\>/\<str:token\>/
        * Searches SO based on the parameters of questions that are tagged 'x', and/or do not have the tags 'y', and/or has a given string or substring in the title

      * stack/get/advanced_search/\<str:page\>/\<str:pagesize\>/\<str:fromdate\>/\<str:todate\>/\<str:order\>/\<str:sort\>/\<str:q\>/\<str:accepted\>/\<str:answers\>/\<str:body\>/\<str:closed\>/\<str:migrated\>/\<str:notice\>/\<str:nottagged\>/\<str:tagged\>/\<str:title\>/\<str:user\>/\<str:url\>/\<str:views\>/\<str:wiki\>/\<str:token\>/
        * Searches SO with comprehensive parameters available to create a tight search pattern.

      * stack/get/all_tags/
        * An internal route that routinely pulls all tags from SO for caching in the DB

      * stack/get/tags_from_site/\<int:pages\>/
        * An internal route that retrieves x number of pages of tags from the SO database

      * stack/get/params/all/
        * An internal route that returns all params that are available for a question in SO

      * stack/get/params/\<str:route\>/
        * An internal route that returns the relevant params to a given route

      * stack/get/routes/
        * An internal route that returns the potential routes a query can take - e.g. question_by_tag, simple_search, etc

      * stack/get/filters/all/
        * An internal route that returns all filters for a SO query

      * stack/get/filters/\<str:route\>/
        * An internal route that returns all filters for a given route

      * stack/get/sort_methods/
        * An internal route that returns all sort methods for an SO query

      * stack/get/order_methods/
        * An internal route that returns all order methods for an SO query

      * stack/get/question_data_fields/
        * An internal route that returns the system-defined data fields for an SO question

    ---

    * *Reddit Routes*

      * reddit/get/query/\<str:search_type\>/\<str:subred\>/\<str:q\>/\<str:limit\>/\<str:token\>/
        * Searches reddit for a given query (q) based on the given parameters of search type (subreddits / posts / comments), a subreddit to search, and a limit of the number of results to return.

      * meta/initialisedb/
        * An internal route that is run once at instantiation of the system to populate the DB with system-critical data, such as SO routes, parameters, and tag lists.

    ---

    * *Local Search Routes*

      * search/stackoverflow/\<str:term\>/
        * Performs a local search for a given term on the cached SO questions

      * search/reddit/\<str:term\>/
        * Perfroms a local search for a given term on the cached Reddit questions

    ---

    * *Search History Routes*

      * searchhistory/\<str:token\>/
        * Retrives the search history of an authenticated user based on their unique hashed identity token

      * searchhistory/retrieve-search-results/\<str:token\>/\<str:term\>/
        * Retrieves the set of results generated by a given, past search term for an authenticated user.
   
* **Project Structure**:
  
  * Each route is assigned a unique view.
  * As a rule, as much data processing as possible is carried out within the view. However, repetetive or complex tasks are passed out to external functions.
  * API calls made to SO and Reddit are handled by individual libraries of functionality, data is requested, retrieved, and sanitised within these functions before being passed back to the view for further processing.
  * Each view utilises a serializer prior to returning the appropriate dataset to the requesting client.
  * In general terms, all serializers serialize all data associated with a data point. i.e. The serialized data is not filtered to just the information required by my own implementation of the front end.
    * This supports the platform intention of being extensible to other devices and use cases where my original front-end design may not mirror the final use-case of the new product.

### Security Measures

* **System Security**

  * The Django configuration is purposely left in a development state as this project is a continuing work-in-progress
  * Production and a properly configured state would see appropriate Django prod settings being implemented, as well as a greater attention to password integrity and authentication for the DB
    * The DB is a standard implementation of Postgres. In a production environment, users with appropriate permissions would be generated to fulfil the needs of the system. e.g. There is no need for the Django platform to have delete access on the DB, users are unable to delete their search history or cached questions. Update access is required due to certain data fields in questions being updated each time they are returned as a part of a search data set.

* **Authentication & Data Integrity**
  * Users are able to access the system in an unauthenticated and an authenticated state.

  * Unauthenticated users are able to use the API lookup service for Reddit and SO, they can also perform a local search for cached data. Unauthenticated users have no access to past search history based on their client, IP, or the history of any other user(s).

  * Authenticated users can use the full functionality of the API lookups and local search; they are also able to view their personal search history and return the original results for any given search.
    * User accounts are secured by a username and password. For development purposes, no constraints have been placed on username or password integrity other than usernames must be unique and passwords must conform to a minimum length.

    * All user accounts have a unique hashed token generated.

    * This token is saved to a device session storage at the point of login; the token is appended to all searches carried out by the user as a part of the standard URL format.

    * If a valid token is present for an API lookup or local search, the token is used to associate the search results with the corresponding user.

    * If a valid token is present for a search history request, the token is used to retrieve the data for the corresponding user.

    * The use of token authentication removes the need for unhashed data to be transmitted over the client-server connection and reduces the risk of data manipulation, interception, and malicious intent.

### Performance Optimisation

* **Task Orchestration**

  * All search requests run in linear fashion and rely upon the system architecture and Django's WSGI app server to manage concurrent calls to the backend service.
 
  * Requests that are passed to SO or Reddit are called asynchronously, but are still orchestrated by the main thread of the Django service.

  * During a user search, when an API service - SO or Reddit - returns a set of results, prior to being serialized and returned to the requesting client, the data is dispatched to the Django RQ framework as a job.
    
    * The RQ framework uses a Redis server instance to cache the job in a queue, which is then processed synchronously in a separate instance of the back-end server.

    * The jobs are all assigned to the 'default' priority queue as all jobs dispatched to the framework hold the same priority.

    * The high-throughput nature of Redis caching in RAM ensures that jobs are processed in a timely fashion and allows for short-term retention of the data set before it is expunged from memory.

    ---
    
    * This queue, operating asynchronously from the main Django service, interrogates the DB to identify which questions from the data set are not represented in the DB and then commits these questions to the DB

    * Questions that are already represented in the DB have fields such as 'number of times returned as a search result' updated.

    ---
   
    * The queue also processes user-authenticated data such as appending a search term and the associated results to the user profile.
   
  * The use of the RQ framework to action these non-critical processes ensures that the main Django service is able to handle the maximum number of user API requests.

### Testing and QA

* A comprehensive unit test suite is implemented to ensure that the platform meets designed criteria.
* Unit tests are auto-run upon push to GitHub
* There are integration tests run between modules of code, specifically between the integration of SO and Reddit API lookups and the Rest Framework handling of client requests.

### Scalability & Maintenance

* **Deployment:**

  * *Small-scale and local deployment*

    * For deployment at a local level, or for code collaboration, a series of Docker containers have been implemented with appropriate networking interfaces.

    * For ease of community implementation of this platform, the docker instance is available in a stable, tested format via the cloud.

  ---

  * *Wider deployment*

    * The application utilises frameworks that are inherently scalable and are intended for deployment on cloud systems that provide scaling support from the ground up.

    * **Deployment and scaling to AWS**

      * For a small user-base where there are no performance limitations imposed on single services such as the DB:

        * Elastic Beanstalk for hosting the Rest Framework and RQ Worker services. Considerations and implications of this:

          * A single EBS instance could run both services via an appropriate config file; however, dependent upon the user-base growth, this may limit the availability of the platform.

          * The current RQ Worker tasks are low resource intensity and would likely not be a significantly limiting factor with this initial platform functionality; however, this may become a more limiting factor if the functionality of the system is expanded in the future.

          * Alternatively, the two services could be run on two EBS instances. This reduces overhead on a single system, but increases cost for the overall platform.

        * Amazon RDS for hosting and handling the PostgreSQL database. This allows for scaling as required, but will also easily manage the needs of a small user-base and the associated DB overheads.

        * Amazon ElasticCache: A performance enhancing service from which to operate the Redis caching functionality of the RQ Worker job queue.

        * There is no current requirement for static media caching, but this could be achieved via the Amazon S3 service if required in a later update.

      * For a larger user-base where scalability of services, especially dynamic scalability is required:

        * EC2 in combination with Auto Scaling and Elastic Load Balancing

          * Provides scaling during peak use hours

          * Provides scaling based on availability zone - providing users with a greater user experience based on their geo-location

          * Improves cost effectiveness.

          * Encryption and decryption can be offloaded from EC2 instances

          * Load balancing can be restricted to HTTP requests as the prevalent protocol in this system

        * Aurora as a scalable and more 'production hardened' platform for Postgres

        * Elasticache for Redis

        * If the system undergoes a full redesign in the future, it could be broken in to a microservice architecture and deployed via Lambda and Gateway.

    * **Deployment and scaling to GCP**

      * For a small user-base:

        * App engine, a single instance will handle both the Rest Framework and RQ Worker instances.

          * App engine also provides robust scaling, allowing for organic growth of the platform without migration to a different system if preferred.

        * CloudSQL for managing PostgreSQL instance

        * Memorystore for managing Redis and in-memory caching

        * Cloud Storage if media storage becomes a requirement
       
      * For a larger user-base:

        * Google Kubernetes Engine - perhaps (definitely!) overkill for a platform like this. However, a GKE cluster would allow for enhanced deployment patterns a more granular control over deployment regions and zones.

          * K8s also allows for enhanced CI/CD pipelines, and a more robust version control system to control update issues.

          * K8s offers vertical as well as horizontal scaling, allowing for increased resources to be directed to an existing pod, rather than spinning up new instances.

        * Cloud Spanner for a distributed DB service.

        * Memorystore for Redis caching

        * Cloud Functions and Gateway if a redesign results in a microservice architecture.
