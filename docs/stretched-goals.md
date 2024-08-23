# Stretched Goals

## 1. https://pokeapi.co has been really unstable lately. How can you ensure your service can deliver even during times of instability?

1. Caching (if static API responses):

   - Store successfully data retrievals (locally/DynamoDB) with TTL.
     Cache API Responses Locally (or in DynamoDB):
   - CloudFront caching
   - Lambda Ephemeral Cache:In-memory Cache: helps with concurrent calls.
   - API Gateway caching (up to 1 hour)

2. Fallback

   - Fallback, pregenerated team
   - Prefetching data in warm lambda?
   - Maintain a DB copy

3. Retry

   - Retries with increasing wait times

4. Rate limiting on API Gateway
   - Prevent overwhelming server by setting limits and respond with Error 429 too many requests

## 2. A spambot has found your service! How can you ensure only people are using your service?

1. CAPTCHA on UI

   - Visible: users solves puzzle
   - Invisible: hidden fields (honeypots), time-based, behavior-based analysis to detect spambots

2. Rate limiting on API Gateway
3. CloudFront WAF blocking based on IP reputation or patterns
4. AWS WAF Bot Control: managed anti-bot rules
5. Add authentications & authorization
6. Session tokens limiting number of actions in a given timeframe

## 3. Our SuperSoccer Showdown has gone viral! How can we handle all of these users?

1. All infra chosen autoscales (gateway, lambdas, DynamoDB)
2. Caching (CDN, Gateway, Lambda ephemeral storage)
3. Keep warm lambdas (Provisioned Concurrency)
4. Deploy in multiple regions


# Potential discussion points
1. The current code isn't ready for Lambda deployment. How would we restructure to prepare for lambda?

2. Stretch point: We want to show the 'soccer team power' which is the sum of a new statistic 'player soccer power', how can we support this?

3. (How I handled errors in _fetch_random_character)
