# Snopes Twitter Bot

## Environment Variables

### TWITTER_API_CLIENT_ID

> OAuth2 client ID.

### TWITTER_API_CLIENT_SECRET

> OAuth2 client secret.

### TWITTER_API_SCOPES

> Comma-separated list of OAuth2 scopes.

### TWITTER_API_REDIRECT_URI

> URI to redirect to after authorizing a Twitter account.

### TWITTER_API_REFRESH_TOKEN_URI

> URI to obtain access tokens.

### TWITTER_API_TOKEN_TIMEOUT

> Timeout, in seconds, before a OAuth token's `expires_at` is considered expired. ie. ```if current_time + timeout >= expires_at, then token is deemed expired```.

### TWITTER_API_SNOPES_QUERY

> A Twitter [query](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query) to select Snopes tweets.

### APP_NAME

> Name of the app.

### APP_ENABLED

> If not set to True, app will exit immediately.

### APP_SNOPES_FACT_CHECK_URI

> URL to Snopes.com's fact check section.

### APP_SNOPES_RATING_FILE

> Path to the `.json` file containing descriptions of each [Snopes rating](https://www.snopes.com/fact-check-ratings/).

### APP_SNOPES_DETAIL_TIMEOUT

> Timeout, in seconds, to allow for a HTTP request to obtain details from a Snopes fact check.

### APP_CHECK_TIMEOUT

> Timeout, in seconds, to check Twitter for new Snopes tweets.

### APP_TWEET_INTERVAL_TIMEOUT

> Timeout, in seconds, to wait after posting a new tweet.
