# Deploying Static Site to www.docsie.io

## Overview

The www.docsie.io static site is deployed via GitHub Actions to S3 and served through CloudFront with Lambda@Edge for language redirects.

## Architecture

```
GitHub Repository (master branch)
    ↓ (on push)
GitHub Actions Workflow
    ↓ (aws s3 sync)
S3 Bucket: www-docsie-io
    ↓ (origin)
CloudFront Distribution: E11O0CNQO6HZL
    ↓ (d2kmf7cf56lmcn.cloudfront.net)
DNS: www.docsie.io
```

## Components

### 1. S3 Buckets

- **Production**: `www-docsie-io`
  - Website endpoint: `www-docsie-io.s3-website-us-east-1.amazonaws.com`
  - Public read access enabled
  - Static website hosting enabled

- **Staging**: `ww7-docsie-io`
  - Website endpoint: `ww7-docsie-io.s3-website-us-east-1.amazonaws.com`
  - Used for testing before production deployment

### 2. CloudFront Distributions

- **Production**: `E11O0CNQO6HZL`
  - Domain: `d2kmf7cf56lmcn.cloudfront.net`
  - Alias: `www.docsie.io`
  - Origin: S3 bucket `www-docsie-io`
  - SSL Certificate: ACM cert `81ea4272-59c2-4db3-8195-5e45364097ae`

- **Staging**: `E3IQ2X1LN0DB5H`
  - Domain: `dolwx8vk6acxt.cloudfront.net`
  - Alias: `ww7.docsie.io`
  - Origin: S3 bucket `ww7-docsie-io`

### 3. Lambda@Edge Function

**Function**: `docsie-language-redirect:1`
- **ARN**: `arn:aws:lambda:us-east-1:652001424605:function:docsie-language-redirect:1`
- **Event Type**: viewer-request
- **Purpose**: 301 redirects for multi-lingual URLs to English versions

**Redirect Rules**:
- Blog URLs: `/blog/{lang}/*` → `/blog/*`
  - Example: `/blog/es/articles/guide` → `/blog/articles/guide`
- Site URLs: `/{lang}/*` → `/*`
  - Example: `/de/features` → `/features`

**Supported Languages**: da, de, es, fr, hu, it, ja, ko, nl, pl, pt-br, pt-pt, ru, sv, tr, zh

### 4. GitHub Actions Deployment

**Workflow**: `.github/workflows/deploy-to-s3.yml`

**Triggers**:
- Push to `master` branch
- Manual dispatch via GitHub UI

**Process**:
1. Checkout repository
2. Configure AWS credentials (from GitHub Secrets)
3. Sync files to S3 (delta-based with `--size-only`)
4. Exclude language folders (handled by Lambda@Edge redirects)
5. Invalidate CloudFront cache
6. Report deployment status

**AWS Credentials** (GitHub Secrets):
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

**IAM User**: `github-actions-docsie-deploy`
- S3 permissions: PutObject, GetObject, DeleteObject, ListBucket
- CloudFront permissions: CreateInvalidation

## Deployment Process

### Automatic Deployment

1. Push changes to `master` branch
2. GitHub Actions automatically triggers
3. Changed files sync to S3
4. CloudFront cache invalidated
5. Site updates within 1-2 minutes

### Manual Deployment

1. Go to GitHub Actions tab
2. Select "Deploy to S3 + CloudFront" workflow
3. Click "Run workflow"
4. Select `master` branch
5. Click "Run workflow" button

## Language Migration Strategy

### One-Time Migration (Completed 2025-11-23)

Previously, the site had multi-lingual content in language-specific folders:
- `/da/`, `/de/`, `/es/`, `/fr/`, etc. (16 languages)
- `/blog/da/`, `/blog/de/`, `/blog/es/`, etc.

**Migration approach**:
1. Lambda@Edge function created to handle 301 redirects
2. Language folders excluded from S3 sync
3. All language URLs automatically redirect to English versions
4. SEO-friendly permanent redirects (301)
5. Cached redirects for 1 year (`max-age=31536000`)

**Why language folders are excluded**:
- CloudFront Function handles all redirects at the edge
- No need to store duplicate/outdated content
- Reduces S3 storage costs
- Faster deployments (only English content synced)
- This was a one-time migration to English-only content

## DNS Configuration

**Route53 Hosted Zone**: `ZYD1PZYW221LV` (docsie.io)

**CNAME Record**:
```
www.docsie.io → d2kmf7cf56lmcn.cloudfront.net
```

**TTL**: 300 seconds

## SSL/TLS

**Certificate**: AWS Certificate Manager (ACM)
- ARN: `arn:aws:acm:us-east-1:652001424605:certificate/81ea4272-59c2-4db3-8195-5e45364097ae`
- Domain: `*.docsie.io` (wildcard)
- Validation: DNS
- Protocol: TLSv1.2_2021 minimum

## Monitoring & Maintenance

### CloudFront Cache

**Default TTL**: 86400 seconds (24 hours)
**Max TTL**: 31536000 seconds (1 year)
**Cache Control**: `public, max-age=31536000` (set in S3 sync)

**Cache Invalidation**:
- Automatic after every deployment
- Path: `/*` (all files)
- Via GitHub Actions workflow

### Checking Deployment Status

**CloudFront Distribution Status**:
```bash
aws cloudfront get-distribution --id E11O0CNQO6HZL --query 'Distribution.Status'
```

**DNS Propagation**:
```bash
dig www.docsie.io CNAME +short
```

**Test Redirects**:
```bash
# Blog article redirect
curl -I https://www.docsie.io/blog/es/articles/test

# Site page redirect
curl -I https://www.docsie.io/de/features
```

### Logs

- **CloudFront Logs**: Not currently enabled
- **Lambda@Edge Logs**: `/aws/lambda/us-east-1.docsie-language-redirect`
- **GitHub Actions Logs**: In GitHub repository Actions tab

## Troubleshooting

### Deployment Failed

1. Check GitHub Actions logs for error messages
2. Verify AWS credentials are valid
3. Confirm S3 bucket permissions
4. Check IAM policy includes required permissions

### Site Not Updating

1. Clear CloudFront cache manually:
   ```bash
   aws cloudfront create-invalidation --distribution-id E11O0CNQO6HZL --paths "/*"
   ```
2. Wait 5-10 minutes for invalidation to complete
3. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

### Redirects Not Working

1. Check Lambda@Edge function is attached to distribution
2. Verify function version is `:1` (not `$LATEST`)
3. Check CloudFront distribution status is "Deployed"
4. Wait 10-30 minutes for Lambda@Edge deployment to edge locations

### DNS Not Resolving

1. Check Route53 CNAME record points to CloudFront domain
2. Verify CloudFront distribution has correct alias
3. Check SSL certificate is valid and attached
4. Wait for DNS propagation (up to 5 minutes)

## Cost Optimization

- **S3 Storage**: Only English content stored (~454 MB)
- **CloudFront**: Pay per request and data transfer
- **Lambda@Edge**: Pay per invocation (redirects cached for 1 year)
- **Route53**: Standard hosted zone pricing

## Security

- **HTTPS Only**: All HTTP traffic redirected to HTTPS
- **S3 Bucket Policy**: Public read-only for website content
- **IAM Least Privilege**: GitHub Actions user has minimal required permissions
- **No Secrets in Code**: AWS credentials stored as GitHub Secrets

## Backup & Recovery

**S3 Bucket Backup**:
- Versioning: Not enabled (static site, version controlled in Git)
- Source of truth: GitHub repository `master` branch
- Recovery: Redeploy from GitHub

**Staging Environment**:
- `ww7.docsie.io` serves as staging/testing environment
- Test changes here before production deployment

## Future Improvements

- [ ] Enable CloudFront access logs for analytics
- [ ] Set up S3 lifecycle policies for old versions
- [ ] Add Slack/email notifications for deployment status
- [ ] Implement blue/green deployments
- [ ] Add performance monitoring (Web Vitals)
- [ ] Consider CloudFront Functions instead of Lambda@Edge for cost savings

---

**Last Updated**: 2025-11-23
**Maintained By**: DevOps Team
