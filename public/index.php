<?php

declare(strict_types=1);

require_once __DIR__ . '/../src/bootstrap.php';

use App\Modules\ProductIntelligenceEngine;
use App\Modules\SmartLandingPageGenerator;
use App\Modules\TrackingEngine;
use App\Modules\ScalingEngine;

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed'], JSON_UNESCAPED_UNICODE);
    exit;
}

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) ?: '/';
$raw = file_get_contents('php://input');
$payload = json_decode($raw ?: '{}', true);

if (!is_array($payload)) {
    http_response_code(422);
    echo json_encode(['error' => 'Invalid JSON body'], JSON_UNESCAPED_UNICODE);
    exit;
}

try {
    $response = match ($path) {
        '/api/product-intelligence' => (new ProductIntelligenceEngine())->analyze($payload),
        '/api/landing-page' => (new SmartLandingPageGenerator())->generate($payload),
        '/api/tracking' => (new TrackingEngine())->evaluate($payload),
        '/api/scaling' => (new ScalingEngine())->decide($payload),
        '/api/tracking-event' => ['ok' => true],
        default => null,
    };

    if ($response === null) {
        http_response_code(404);
        echo json_encode(['error' => 'Endpoint not found'], JSON_UNESCAPED_UNICODE);
        exit;
    }

    echo json_encode($response, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
} catch (InvalidArgumentException $e) {
    http_response_code(422);
    echo json_encode(['error' => $e->getMessage()], JSON_UNESCAPED_UNICODE);
}
