# Results
## Load data
```
import pandas
d = pandas.read_csv('visits.csv')
```
## Mean emotions

Positions with biggest happiness:
```
d[['position', 'happiness']].groupby(['position']).mean().sort_values('happiness', ascending=False).head()
```
```
happiness                          position                                   
D2.преп-стажер                     1.000000
директор, C9.преп                  1.000000
куратор параллели K                0.999995
исполнительный директор, D1.преп   0.901091
завуч олимпиадного отделения       0.900146
```

Positions with smallest happiness:
```
d[['position', 'happiness']].groupby(['position']).mean().sort_values('happiness').head()
```
```
happiness                                           position
зам. директора по вопросам оформления документо...  7.840994e-20
A1.преп-стажер                                      1.499667e-19
завуч, B9.преп                                      5.665062e-10
контроль питания                                    6.604289e-08
завуч, B7.преп                                      8.669356e-08
```

Positions with biggest neutral:
```
d[['position', 'neutral']].groupby(['position']).mean().sort_values('neutral', ascending=False).head()
```
```
neutral                                         position                                                
контроль питания                                0.999959
A2.преп-стажер                                  0.997640
зам. директора по финансовым вопросам, D1.преп  0.995909
финансовый директор, C3.преп                    0.975927
A+.преп                                         0.956075
```

Positions with biggest sadness:
```
d[['position', 'sadness']].groupby(['position']).mean().sort_values('sadness', ascending=False).head()
```
```
зам. директора по вопросам оформления документо...  1.000000
A1.преп-стажер                                      0.999998
завуч, B7.преп                                      0.999990
C'.преп                                             0.999842
завуч, C1.py.преп                                   0.999253
```
## Emotions by years
Happiness by years:
![bar](http://i.imgur.com/ZKyPWGQ.png)
![line](http://i.imgur.com/PbdEiKy.png)
