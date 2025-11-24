# Language Redirects Tutorial

## Overview

This tutorial explains how the Lambda@Edge redirect system works for www.docsie.io, including how to modify, test, and deploy changes to the redirect logic.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [How Redirects Work](#how-redirects-work)
3. [Current Configuration](#current-configuration)
4. [Modifying Redirect Logic](#modifying-redirect-logic)
5. [Testing Redirects](#testing-redirects)
6. [Deployment Process](#deployment-process)
7. [Troubleshooting](#troubleshooting)
8. [References](#references)

---

## System Architecture

### Components

```
User Request
    ↓
CloudFront Distribution (E11O0CNQO6HZL for www.docsie.io)
    ↓
Lambda@Edge (viewer-request event)
    ↓
[Check if URL matches redirect pattern]
    ↓
    ├─→ Match: Return 301 redirect
    └─→ No match: Continue to S3 origin
```

### Key Resources

- **Lambda Function**: `docsie-language-redirect`
- **Current Version**: `:2` (Site redirects only, blog excluded)
- **Function ARN**: `arn:aws:lambda:us-east-1:652001424605:function:docsie-language-redirect:2`
- **IAM Role**: `docsie-language-redirect-lambda-edge`
- **Event Type**: `viewer-request` (runs before request reaches origin)
- **CloudFront Distributions**:
  - Production: `E11O0CNQO6HZL` (www.docsie.io)
  - Staging: `E3IQ2X1LN0DB5H` (ww7.docsie.io)

---

## How Redirects Work

### Execution Flow

1. **User makes request**: `https://www.docsie.io/de/features`
2. **CloudFront receives request** at edge location
3. **Lambda@Edge triggers** on `viewer-request` event
4. **Lambda checks URI** against redirect patterns
5. **If match found**:
   - Returns 301 response with `Location: /features`
   - Sets `Cache-Control: max-age=31536000` (1 year)
   - Response cached at edge location
6. **If no match**:
   - Request continues to S3 origin
   - Normal content delivery

### Current Redirect Rules (Version 2)

**Site Language Redirects** (Active):
- Pattern: `/{lang}/*` → `/*`
- Example: `/de/features` → `/features`
- Example: `/es/pricing` → `/pricing`
- Example: `/fr/` → `/`

**Blog Redirects** (Disabled in v2):
- Pattern: `/blog/{lang}/*` → `/blog/*`
- Status: **Removed** - blog language URLs are preserved

**Supported Languages**:
```javascript
['da', 'de', 'es', 'fr', 'hu', 'it', 'ja', 'ko', 'nl',
 'pl', 'pt-br', 'pt-pt', 'ru', 'sv', 'tr', 'zh']
```

### Lambda Function Code

**Location**: `/tmp/language-redirect-lambda.js` (during deployment)

**Current Implementation** (v2):

```javascript
'use strict';

exports.handler = async (event) => {
    const request = event.Records[0].cf.request;
    const uri = request.uri;

    // List of language codes to redirect
    const languages = ['da', 'de', 'es', 'fr', 'hu', 'it', 'ja', 'ko', 'nl',
                       'pl', 'pt-br', 'pt-pt', 'ru', 'sv', 'tr', 'zh'];

    // Note: Blog redirects removed - blog language URLs are kept as-is
    // Only site-level language folders are redirected

    // Check for site language folder URLs: /{lang}/* -> /*
    for (const lang of languages) {
        if (uri.startsWith(`/${lang}/`)) {
            const redirectPath = uri.substring(lang.length + 1); // Remove /{lang}
            return {
                status: '301',
                statusDescription: 'Moved Permanently',
                headers: {
                    'location': [{
                        key: 'Location',
                        value: redirectPath
                    }],
                    'cache-control': [{
                        key: 'Cache-Control',
                        value: 'max-age=31536000'
                    }]
                }
            };
        }

        // Also handle root language URLs: /{lang} -> /
        if (uri === `/${lang}` || uri === `/${lang}/`) {
            return {
                status: '301',
                statusDescription: 'Moved Permanently',
                headers: {
                    'location': [{
                        key: 'Location',
                        value: '/'
                    }],
                    'cache-control': [{
                        key: 'Cache-Control',
                        value: 'max-age=31536000'
                    }]
                }
            };
        }
    }

    // No redirect needed, continue with original request
    return request;
};
```

---

## Current Configuration

### Production (www.docsie.io)

```yaml
CloudFront Distribution: E11O0CNQO6HZL
Domain: d2kmf7cf56lmcn.cloudfront.net
Alias: www.docsie.io
Origin: www-docsie-io.s3-website-us-east-1.amazonaws.com
Lambda@Edge: docsie-language-redirect:2
SSL Certificate: arn:aws:acm:us-east-1:652001424605:certificate/81ea4272-59c2-4db3-8195-5e45364097ae
```

### Staging (ww7.docsie.io)

```yaml
CloudFront Distribution: E3IQ2X1LN0DB5H
Domain: dolwx8vk6acxt.cloudfront.net
Alias: ww7.docsie.io
Origin: ww7-docsie-io.s3-website-us-east-1.amazonaws.com
Lambda@Edge: docsie-language-redirect:2
SSL Certificate: arn:aws:acm:us-east-1:652001424605:certificate/81ea4272-59c2-4db3-8195-5e45364097ae
```

---

## Modifying Redirect Logic

### Step 1: Update Lambda Function Code

1. **Edit the function**:
   ```bash
   # Create/edit the Lambda function file
   vim /tmp/language-redirect-lambda.js
   ```

2. **Make your changes**:
   - Add new redirect patterns
   - Modify existing patterns
   - Change redirect destinations
   - Update language list

3. **Example: Re-enable blog redirects**:
   ```javascript
   // Add before the site redirects section
   const blogMatch = uri.match(/^\/blog\/(da|de|es|fr|hu|it|ja|ko|nl|pl|pt-br|pt-pt|ru|sv|tr|zh)\/(.+)$/);
   if (blogMatch) {
       const redirectPath = `/blog/${blogMatch[2]}`;
       return {
           status: '301',
           statusDescription: 'Moved Permanently',
           headers: {
               'location': [{ key: 'Location', value: redirectPath }],
               'cache-control': [{ key: 'Cache-Control', value: 'max-age=31536000' }]
           }
       };
   }
   ```

### Step 2: Package and Upload

```bash
# Create deployment package
cd /tmp
zip language-redirect-lambda.zip language-redirect-lambda.js

# Update Lambda function code
aws lambda update-function-code \
  --function-name docsie-language-redirect \
  --zip-file fileb:///tmp/language-redirect-lambda.zip \
  --region us-east-1
```

### Step 3: Publish New Version

```bash
# Publish a new version (e.g., version 3)
aws lambda publish-version \
  --function-name docsie-language-redirect \
  --region us-east-1 \
  --description "v3 - Your description here"
```

**Note the version number** returned (e.g., `:3`)

### Step 4: Update CloudFront Distributions

**For Production (www.docsie.io)**:

```bash
# Get current config
aws cloudfront get-distribution-config \
  --id E11O0CNQO6HZL \
  --query 'DistributionConfig' \
  > /tmp/www-dist-config.json

# Edit the config to change Lambda version
# Find: "LambdaFunctionARN": "...function/docsie-language-redirect:2"
# Change to: "LambdaFunctionARN": "...function/docsie-language-redirect:3"

# Get ETag
ETAG=$(aws cloudfront get-distribution-config \
  --id E11O0CNQO6HZL \
  --query 'ETag' \
  --output text)

# Update distribution
aws cloudfront update-distribution \
  --id E11O0CNQO6HZL \
  --distribution-config file:///tmp/www-dist-config.json \
  --if-match "$ETAG"
```

**Repeat for Staging** (E3IQ2X1LN0DB5H)

### Step 5: Wait for Deployment

```bash
# Check deployment status
aws cloudfront get-distribution --id E11O0CNQO6HZL --query 'Distribution.Status'

# Wait for "Deployed" status (typically 10-30 minutes)
```

---

## Testing Redirects

### Test Locally (Before Deployment)

```bash
# Test the Lambda function locally with AWS SAM or Node.js
node -e "
const handler = require('/tmp/language-redirect-lambda.js').handler;
const event = {
  Records: [{
    cf: {
      request: {
        uri: '/de/features'
      }
    }
  }]
};
handler(event).then(console.log);
"
```

### Test on Staging (ww7.docsie.io)

```bash
# Test site redirect
curl -I https://ww7.docsie.io/de/features

# Expected response:
# HTTP/2 301
# location: /features
# x-cache: LambdaGeneratedResponse from cloudfront

# Test blog URL (should NOT redirect in v2)
curl -I https://ww7.docsie.io/blog/es/articles/test

# Expected response:
# HTTP/2 404 (or 200 if content exists)
# No redirect
```

### Test on Production (www.docsie.io)

```bash
# After staging tests pass, test production
curl -I https://www.docsie.io/de/features
curl -I https://www.docsie.io/fr/pricing
curl -I https://www.docsie.io/es/
```

### Verify Response Headers

**Successful redirect should show**:
```
HTTP/2 301
location: /features
cache-control: max-age=31536000
x-cache: LambdaGeneratedResponse from cloudfront
```

**Key indicators**:
- `301`: Permanent redirect (SEO-friendly)
- `x-cache: LambdaGeneratedResponse`: Lambda@Edge is working
- `cache-control`: Response is cached for 1 year

---

## Deployment Process

### Quick Reference Commands

```bash
# 1. Update function code
aws lambda update-function-code \
  --function-name docsie-language-redirect \
  --zip-file fileb:///tmp/language-redirect-lambda.zip \
  --region us-east-1

# 2. Publish new version
VERSION=$(aws lambda publish-version \
  --function-name docsie-language-redirect \
  --region us-east-1 \
  --description "Your description" \
  --query 'Version' \
  --output text)

echo "Published version: $VERSION"

# 3. Update staging distribution
./update-cloudfront-lambda.sh E3IQ2X1LN0DB5H $VERSION

# 4. Test staging
curl -I https://ww7.docsie.io/de/test

# 5. Update production distribution
./update-cloudfront-lambda.sh E11O0CNQO6HZL $VERSION

# 6. Test production
curl -I https://www.docsie.io/de/test
```

### Rollback Procedure

If a new version causes issues:

```bash
# Rollback to previous version (e.g., from v3 to v2)
# Update CloudFront to use the old version ARN

# Get current config
aws cloudfront get-distribution-config \
  --id E11O0CNQO6HZL \
  > /tmp/rollback-config.json

# Edit: Change :3 back to :2 in LambdaFunctionARN

# Get ETag and update
ETAG=$(aws cloudfront get-distribution-config \
  --id E11O0CNQO6HZL \
  --query 'ETag' \
  --output text)

aws cloudfront update-distribution \
  --id E11O0CNQO6HZL \
  --distribution-config file:///tmp/rollback-config.json \
  --if-match "$ETAG"
```

---

## Troubleshooting

### Redirects Not Working

**Symptoms**: Language URLs return 200 instead of 301

**Possible Causes**:
1. Lambda@Edge not attached to distribution
2. Using `$LATEST` instead of published version
3. CloudFront still deploying (InProgress)
4. Cached old response at edge location

**Solutions**:

```bash
# 1. Check Lambda association
aws cloudfront get-distribution-config \
  --id E11O0CNQO6HZL \
  --query 'DistributionConfig.DefaultCacheBehavior.LambdaFunctionAssociations'

# Should show:
# {
#   "Quantity": 1,
#   "Items": [{
#     "LambdaFunctionARN": "...function/docsie-language-redirect:2",
#     "EventType": "viewer-request"
#   }]
# }

# 2. Check deployment status
aws cloudfront get-distribution \
  --id E11O0CNQO6HZL \
  --query 'Distribution.Status'

# Should return: "Deployed"

# 3. Invalidate cache
aws cloudfront create-invalidation \
  --distribution-id E11O0CNQO6HZL \
  --paths "/*"

# 4. Test with cache bypass
curl -I -H "Cache-Control: no-cache" https://www.docsie.io/de/features
```

### Wrong Redirect Destination

**Symptoms**: Redirect goes to wrong URL

**Debug**:

```bash
# Check Lambda logs
aws logs tail /aws/lambda/us-east-1.docsie-language-redirect \
  --follow \
  --format short

# Test specific URL
curl -I https://www.docsie.io/de/features 2>&1 | grep -i location

# Should show: location: /features
```

### Lambda Function Errors

**Symptoms**: 502 Bad Gateway or 500 errors

**Debug**:

```bash
# Check Lambda logs for errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/us-east-1.docsie-language-redirect \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --query 'events[*].message' \
  --output text

# Common issues:
# - Syntax errors in JavaScript
# - Incorrect event structure
# - Timeout (increase timeout setting)
# - Memory limit (increase memory setting)
```

### CloudFront Distribution Conflict

**Symptoms**: "Can't have both CloudFront Function and Lambda@Edge for same event type"

**Solution**:

```bash
# Remove CloudFront Function first
aws cloudfront get-distribution-config \
  --id E11O0CNQO6HZL \
  > /tmp/fix-config.json

# Edit file: Set FunctionAssociations.Quantity to 0
# Remove Items array under FunctionAssociations

# Update distribution
ETAG=$(aws cloudfront get-distribution-config \
  --id E11O0CNQO6HZL \
  --query 'ETag' \
  --output text)

aws cloudfront update-distribution \
  --id E11O0CNQO6HZL \
  --distribution-config file:///tmp/fix-config.json \
  --if-match "$ETAG"
```

---

## References

### Main Documentation

- **Deployment Guide**: `DEPLOYING_STATIC_SITE.md` - Main deployment documentation
- **This Tutorial**: `LANGUAGE_REDIRECTS_TUTORIAL.md` - You are here

### Related Docsie.io Documentation

For the main Docsie.io application (Django), see these CLAUDE.md files:

1. **`/Users/philippetrounev/PycharmProjects/docsie.io/CLAUDE.md`**
   - Main system overview
   - References to all modules and CLAUDE.md files

2. **`/Users/philippetrounev/PycharmProjects/docsie.io/docsie/api/deployments/CLAUDE.md`**
   - Deployment system for documentation portals
   - Custom domain management
   - CloudFront integration examples

3. **`/Users/philippetrounev/PycharmProjects/docsie.io/docsie/files/CLAUDE.md`**
   - File management and S3 integration
   - S3 bucket policies and access

### AWS Resources

- **Lambda@Edge Documentation**: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-at-edge.html
- **CloudFront Distributions**: https://console.aws.amazon.com/cloudfront/
- **Lambda Functions**: https://console.aws.amazon.com/lambda/
- **Route53 DNS**: https://console.aws.amazon.com/route53/

### Version History

| Version | Date | Description | Redirect Rules |
|---------|------|-------------|----------------|
| v1 | 2025-11-23 | Initial version | Blog + Site redirects |
| v2 | 2025-11-24 | Blog redirects removed | Site redirects only |

### Current Lambda Versions

```bash
# List all versions
aws lambda list-versions-by-function \
  --function-name docsie-language-redirect \
  --region us-east-1 \
  --query 'Versions[*].[Version,Description]' \
  --output table

# Output:
# ┌─────────┬───────────────────────────────────────┐
# │ Version │ Description                           │
# ├─────────┼───────────────────────────────────────┤
# │ 1       │ v1 - Blog and site redirects          │
# │ 2       │ v2 - Site redirects only              │
# └─────────┴───────────────────────────────────────┘
```

---

## Best Practices

### Development Workflow

1. **Always test on staging first** (ww7.docsie.io)
2. **Use versioned Lambda deployments** (never use `$LATEST` in production)
3. **Document version changes** in commit messages and version descriptions
4. **Monitor CloudWatch logs** after deployment
5. **Keep rollback procedure handy**

### Performance Optimization

1. **Cache redirects for maximum duration**: `max-age=31536000`
2. **Use simple pattern matching**: Avoid complex regex when possible
3. **Return early**: Check most common patterns first
4. **Minimize Lambda code size**: Keep dependencies minimal

### Security Considerations

1. **IAM Role Least Privilege**: Lambda execution role only has necessary permissions
2. **Validate input**: Always validate URIs before processing
3. **Rate limiting**: CloudFront provides DDoS protection
4. **Logging**: Keep CloudWatch Logs enabled for audit trail

---

## Quick Reference Card

```bash
# Update Lambda code
aws lambda update-function-code \
  --function-name docsie-language-redirect \
  --zip-file fileb:///tmp/language-redirect-lambda.zip \
  --region us-east-1

# Publish version
aws lambda publish-version \
  --function-name docsie-language-redirect \
  --region us-east-1 \
  --description "Your description"

# Check distribution status
aws cloudfront get-distribution \
  --id E11O0CNQO6HZL \
  --query 'Distribution.Status'

# Test redirect
curl -I https://www.docsie.io/de/features

# View logs
aws logs tail /aws/lambda/us-east-1.docsie-language-redirect --follow

# Invalidate cache
aws cloudfront create-invalidation \
  --distribution-id E11O0CNQO6HZL \
  --paths "/*"
```

---

**Last Updated**: 2025-11-24
**Maintained By**: DevOps Team
**Questions?**: Refer to DEPLOYING_STATIC_SITE.md or main Docsie.io CLAUDE.md documentation
