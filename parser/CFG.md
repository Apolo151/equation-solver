# Context Free Grammar
1. S → Expression
2. Expression → Term Expression'
3. Expression' → + Term Expression' | - Term Expression' | ε
4. Term → Factor Term'
5. Term' → * Factor Term' | / Factor Term' | ε
6. Factor → Power Factor'
7. Factor' → ^ Power Factor' | ε
8. Power → Function | Primary
9. Function → sqrt( Expression ) | log10( Expression )
10. Primary → ( Expression ) | Number | Variable
11. Number → Digit Number'
12. Number' → Digit Number' | . Digit Sequence | ε
13. Digit Sequence → Digit Digit Sequence | ε
14. Digit → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
15. Variable → x