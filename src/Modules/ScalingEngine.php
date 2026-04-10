<?php

declare(strict_types=1);

namespace App\Modules;

final class ScalingEngine
{
    public function decide(array $input): array
    {
        $roas = (float) ($input['roas'] ?? 0);
        $cvr = (float) ($input['cvr'] ?? 0);
        $status = strtoupper(trim((string) ($input['status'] ?? 'TESTING')));

        if ($roas > 1.5 && $cvr > 3) {
            return [
                'decision' => 'SCALE_AGGRESSIVELY',
                'reason' => 'ROAS and CVR both exceed winner thresholds, indicating profitable demand.',
                'next_action' => 'Duplicate winning ad sets, expand audiences, and raise budget 30-50% every 48 hours.',
                'budget_recommendation' => 'Increase daily budget by 30% now and monitor hourly profitability.',
            ];
        }

        if ($roas < 1.0 || $status === 'DEAD') {
            return [
                'decision' => 'KILL_FAST',
                'reason' => 'Profitability is below break-even with weak conversion signal.',
                'next_action' => 'Pause campaigns and replace angle, creative hook, or offer before relaunch.',
                'budget_recommendation' => 'Cut budget to zero immediately.',
            ];
        }

        return [
            'decision' => 'ITERATE',
            'reason' => 'Mixed signal; there may be upside after offer and landing optimization.',
            'next_action' => 'Test 2-3 new angles and pricing options, then re-evaluate after 1,000 clicks.',
            'budget_recommendation' => 'Hold budget flat until ROAS clears 1.5.',
        ];
    }
}
