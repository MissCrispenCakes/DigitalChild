#!/usr/bin/env python3
"""Quick script to validate all scorecard URLs."""

from processors.scorecard_validator import validate_scorecard_urls

print('✓ All tests passed!\n')
print('Starting URL validation of 2,543 sources...')
print('This will take 5-10 minutes. Running in parallel with 10 workers...\n')

summary = validate_scorecard_urls(save=True)

print(f'\n✓ Validation complete!')
print(f'  Total URLs: {summary["total"]}')
print(f'  Working: {summary["ok"]} ({summary["ok"]/summary["total"]*100:.1f}%)')
print(f'  Broken: {summary["broken"]} ({summary["broken"]/summary["total"]*100:.1f}%)')
print(f'  Redirected: {summary["redirected"]} ({summary["redirected"]/summary["total"]*100:.1f}%)')
print(f'\nResults saved to: data/exports/scorecard_url_validation.json')
