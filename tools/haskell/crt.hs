import Data.Maybe

euclid a b
    | residue == 0 = b
    | otherwise = euclid b residue
    where residue = a `mod` b

extendedEuclid a b = extendedEuclid' a b 1 0 0 1

extendedEuclid' r0 r1 s0 s1 t0 t1
    | residue == 0 = (r1, s1, t1)
    | otherwise = extendedEuclid' r1 residue s1 (s0 - quotient * s1) t1 (t0 - quotient * t1)
    where (quotient, residue) = r0 `divMod` r1

unsafeBasicCrt' r1 n1 r2 n2 = r1 * m2 * n2 + r2 * m1 * n1
    where (_, m1, m2) = extendedEuclid n1 n2

basicCrt' (r1, n1) (r2, n2)
    | common == 1 = Just (unsafeBasicCrt' r1 n1 r2 n2 `mod` (n1 * n2), n1 * n2)
    | diff /= r2 `mod` common = Nothing
    | otherwise = Just ((unsafeBasicCrt' r1' n1' r2' n2' * common + diff) `mod` (n1 * n2 `div` common), n1 * n2 `div` common)
    where common = euclid n1 n2
          n1' = n1 `div` common
          n2' = n2 `div` common
          diff = r1 `mod` common
          r1' = (r1 - diff) `div` common
          r2' = (r2 - diff) `div` common

basicCrt a@(r1, n1) b@(r2, n2)
    | n1 == n2 = if r1 == r2 then Just a else Nothing
    | n1 > n2 = basicCrt' a b
    | otherwise = basicCrt' b a

unsafeCrt xs
    | length xs == 1 = head xs
    | otherwise = unsafeCrt (fromJust (basicCrt a b) : c)
    where a = head xs
          b = head $ tail xs
          c = tail $ tail xs

crt xs
    | length xs == 1 = Just $ head xs
    | isNothing result = Nothing
    | otherwise = crt $ fromJust result : c
    where a = head xs
          b = head $ tail xs
          c = tail $ tail xs
          result = basicCrt a b
