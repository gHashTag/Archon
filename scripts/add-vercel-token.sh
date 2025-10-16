#!/bin/bash
# Script to add VERCEL_TOKEN to GitHub Secrets

set -e

echo "📝 Add VERCEL_TOKEN to GitHub Secrets"
echo "======================================"
echo ""
echo "Steps:"
echo "1. Open https://vercel.com/account/tokens"
echo "2. Click 'Create Token'"
echo "3. Name: 'GitHub Actions'"
echo "4. Scope: 'Full Account'"
echo "5. Copy the token"
echo ""
read -p "Have you created the token? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled. Please create a token first."
    exit 1
fi

echo ""
read -sp "Paste your Vercel token: " VERCEL_TOKEN
echo ""

if [ -z "$VERCEL_TOKEN" ]; then
    echo "❌ Error: Token cannot be empty"
    exit 1
fi

echo ""
echo "Adding VERCEL_TOKEN to GitHub repository gHashTag/Archon..."
gh secret set VERCEL_TOKEN --body "$VERCEL_TOKEN" --repo gHashTag/Archon

echo ""
echo "✅ VERCEL_TOKEN added successfully!"
echo ""
echo "Verifying all secrets are set..."
gh secret list --repo gHashTag/Archon

echo ""
echo "🎉 All Vercel secrets configured!"
echo ""
echo "Next steps:"
echo "1. Commit your changes: git add . && git commit -m 'Add Vercel deployment'"
echo "2. Push to main: git push origin main"
echo "3. GitHub Actions will automatically deploy to Vercel!"
