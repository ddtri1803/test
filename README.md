# V11 Performance Marketing Engine

Lightweight PHP 8.3 system for dropshipping conversion workflows:

1. Product input
2. Niche + angle analysis
3. Landing-page JSON generation
4. Deploy-ready slug output (`/product:[slug]` convention)
5. Ads run externally (Meta/TikTok)
6. Tracking evaluation (`view/click/purchase`)
7. Optimize, kill, or scale

## API Endpoints

- `POST /api/product-intelligence`
- `POST /api/landing-page`
- `POST /api/tracking`
- `POST /api/scaling`

## Local Run

```bash
php -S 127.0.0.1:8080 -t public
```

## Example

```bash
curl -X POST http://127.0.0.1:8080/api/landing-page \
  -H 'Content-Type: application/json' \
  -d '{
    "product_name":"Posture Corrector Pro",
    "niche":"Back Pain Relief",
    "angle":"Pain to confidence transformation",
    "price":"$39.99",
    "audience":"Remote workers",
    "pain_point":"constant back tension after long desk hours",
    "emotion_trigger":"frustration and fear of long-term pain"
  }'
```
