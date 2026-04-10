<?php

declare(strict_types=1);

namespace App\Modules;

use InvalidArgumentException;

final class ProductIntelligenceEngine
{
    public function analyze(array $input): array
    {
        $productName = trim((string) ($input['product_name'] ?? ''));
        $niche = trim((string) ($input['niche'] ?? 'General Wellness'));
        $angle = trim((string) ($input['angle'] ?? 'Pain-to-relief transformation'));

        if ($productName === '') {
            throw new InvalidArgumentException('product_name is required');
        }

        $audience = (string) ($input['target_audience'] ?? 'Impulse buyers who want fast, visible outcomes');
        $painPoint = (string) ($input['pain_point'] ?? 'Daily frustration with a recurring problem and no reliable fix');
        $emotionTrigger = (string) ($input['emotion_trigger'] ?? 'Fear of wasting time and desire for immediate relief');
        $priceSuggestion = (string) ($input['price_suggestion'] ?? '$29.99 - $49.99');

        return [
            'product_name' => $productName,
            'niche' => $niche,
            'angle' => $angle,
            'target_audience' => $audience,
            'pain_point' => $painPoint,
            'emotion_trigger' => $emotionTrigger,
            'price_suggestion' => $priceSuggestion,
            'conversion_potential' => $this->scorePotential($painPoint, $emotionTrigger),
        ];
    }

    private function scorePotential(string $painPoint, string $emotionTrigger): int
    {
        $score = 5;

        if (str_contains(strtolower($painPoint), 'daily') || str_contains(strtolower($painPoint), 'urgent')) {
            $score += 2;
        }

        if (str_contains(strtolower($emotionTrigger), 'fear') || str_contains(strtolower($emotionTrigger), 'relief')) {
            $score += 2;
        }

        return max(1, min(10, $score));
    }
}
