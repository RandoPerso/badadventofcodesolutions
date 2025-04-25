main = do
    print $ extendedEuclid 27 18

euclid a b
    | residue == 0 = b
    | otherwise = euclid b residue
    where residue = a `mod` b

extendedEuclid a b = extendedEuclid' a b 1 0 0 1

extendedEuclid' r0 r1 s0 s1 t0 t1
    | residue == 0 = (r1, s1, t1)
    | otherwise = extendedEuclid' r1 residue s1 (s0 - quotient * s1) t1 (t0 - quotient * t1)
    where (quotient, residue) = r0 `divMod` r1

basicCrt r1 n1 r2 n2 = r1 * m2 * n2 + r2 * m1 * n1
    where (_, m1, m2) = extendedEuclid n1 n2


