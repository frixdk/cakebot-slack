# cakebot-slack

This bot is based on the original cakealgorithm below:

```python
from collections import defaultdict

meetings = [
    {"kage": "thomas", "deltagere": ["frederik", "karsten", "thomas", "kenneth"]}
]

ratios = defaultdict(lambda: defaultdict(float))

for meeting in meetings:
    ratios[meeting['kage']]['given'] += 1.0

    for deltager in meeting['deltagere']:
        ratios[deltager]['eaten'] += 1.0 / len(meeting['deltagere'])
        ratios[deltager]['ratio'] = ratios[deltager]['given'] / ratios[deltager]['eaten']

for ratio in sorted(ratios.items(), key=lambda x: x[1]['ratio']):
    print(ratio[0], ratio[1]['ratio'])

```
