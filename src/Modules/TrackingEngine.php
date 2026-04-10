<?php

declare(strict_types=1);

namespace App\Modules;

final class TrackingEngine
{
    public function evaluate(array $input): array
    {
        $views = max(0.0, (float) ($input['views'] ?? 0));
        $clicks = max(0.0, (float) ($input['clicks'] ?? 0));
        $purchases = max(0.0, (float) ($input['purchases'] ?? 0));
        $adSpend = max(0.0, (float) ($input['ad_spend'] ?? 0));
        $revenue = max(0.0, (float) ($input['revenue'] ?? 0));

        $ctr = $views > 0 ? ($clicks / $views) * 100 : 0;
        $cvr = $clicks > 0 ? ($purchases / $clicks) * 100 : 0;
        $roas = $adSpend > 0 ? $revenue / $adSpend : 0;

        $status = 'DEAD';
        $action = 'KILL';
        $insight = 'Unprofitable signal; stop spend and rework offer angle.';

        if ($roas > 1.5 && $cvr > 3.0) {
            $status = 'WINNER';
            $action = 'SCALE';
            $insight = 'Profitable conversion engine detected; increase budget while holding CPA guardrails.';
        } elseif ($roas > 1.0 || $cvr > 2.0) {
            $status = 'TESTING';
            $action = 'ITERATE';
            $insight = 'Partial signal exists; test new hooks, pricing, and creatives before scaling.';
        }

        return [
            'ctr' => number_format($ctr, 2) . '%',
            'cvr' => number_format($cvr, 2) . '%',
            'roas' => number_format($roas, 2),
            'status' => $status,
            'insight' => $insight,
            'action' => $action,
        ];
    }
}
