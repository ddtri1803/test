<?php

declare(strict_types=1);

namespace App\Modules;

use InvalidArgumentException;

final class SmartLandingPageGenerator
{
    public function generate(array $input): array
    {
        $productName = trim((string) ($input['product_name'] ?? ''));
        $niche = trim((string) ($input['niche'] ?? ''));
        $angle = trim((string) ($input['angle'] ?? ''));
        $price = trim((string) ($input['price'] ?? '$39.99'));
        $audience = trim((string) ($input['audience'] ?? ''));
        $painPoint = trim((string) ($input['pain_point'] ?? ''));
        $emotionTrigger = trim((string) ($input['emotion_trigger'] ?? ''));

        if ($productName === '' || $niche === '' || $angle === '') {
            throw new InvalidArgumentException('product_name, niche, and angle are required');
        }

        $slug = $this->slugify($productName);
        $headline = sprintf('Still struggling with %s? %s ends it fast.', strtolower($painPoint ?: 'the same daily pain'), $productName);

        return [
            'slug' => $slug,
            'headline' => $headline,
            'subheadline' => sprintf('Built for %s who want %s without guesswork.', $audience ?: 'buyers', strtolower($emotionTrigger ?: 'fast relief')),
            'hero' => [
                'title' => sprintf('%s for %s', $productName, $niche),
                'description' => sprintf('Use the %s angle to turn hesitation into action. Price today: %s.', $angle, $price),
                'cta' => 'Claim Discount',
            ],
            'problem_section' => sprintf('Your audience is tired of %s and losing confidence every day.', $painPoint ?: 'slow results'),
            'solution_section' => sprintf('%s delivers a simple, fast routine that creates a visible win in minutes.', $productName),
            'benefits' => [
                'Feel immediate relief and regain control today',
                'Save time and stop wasting money on failed alternatives',
                'Build confidence with a repeatable daily result',
            ],
            'how_it_works' => [
                sprintf('Step 1: Start using %s right out of the box', $productName),
                'Step 2: Follow the quick routine for immediate effect',
                'Step 3: Repeat daily to lock in consistent outcomes',
            ],
            'social_proof' => [
                '“I felt the difference in the first use.”',
                '“This is the first product that actually solved it.”',
                '“I wish I had found this months ago.”',
            ],
            'urgency' => '48-hour launch discount + limited stock remaining.',
            'faq' => [
                'How soon will I see results? Most users notice a change on day one.',
                'Is it beginner-friendly? Yes, setup takes only a few minutes.',
                'What if it does not work for me? Use our 30-day satisfaction guarantee.',
            ],
            'final_cta' => 'Get Relief Now',
            'seo' => [
                'title' => sprintf('%s | Fast %s Relief', $productName, $niche),
                'description' => sprintf('Discover %s and solve %s fast. Limited-time offer available now.', $productName, strtolower($painPoint ?: 'your daily pain')),
                'keywords' => [$productName, $niche, 'limited-time offer', 'quick relief'],
            ],
        ];
    }

    private function slugify(string $value): string
    {
        $slug = strtolower(trim(preg_replace('/[^A-Za-z0-9-]+/', '-', $value) ?? 'product', '-'));
        return $slug !== '' ? $slug : 'product';
    }
}
