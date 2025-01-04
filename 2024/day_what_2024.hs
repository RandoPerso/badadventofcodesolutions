import System.IO

main = do
    putStrLn "Please input the path to the input file"
    inputFilePath <- getLine
    inputFile <- openFile inputFilePath ReadMode
    contents <- hGetContents inputFile
    let beats = convertBeats (lines contents)
    let firstSame = findNext beats 0
    print firstSame
    print (countAll beats 0 0 (-1) 1 firstSame)

convertBeats beats = [ convertLine line 0 0 | line <- beats ]

convertLine [] subtotal offset = (subtotal, offset)
convertLine (char:line) subtotal offset = convertLine line (subtotal + if char == '>' then 1 else 2) (if char == 'O' then subtotal else offset)

findNext beats current = if check beats current then current else findNext beats (current + 1)

check beats x
  = foldr
      (\ beat -> (&&) ((x `mod` fst beat) == snd beat)) True beats

countAll beats currentTime currentAngle previousHit total limit
  | currentTime > limit = total
  | checkAny beats currentTime = if previousHit == -1 then
                countAll beats (currentTime + 1) currentAngle currentTime total limit
            else
                countAll beats (currentTime + 1) (((currentTime - previousHit) * 30 + currentAngle - 180) `mod` 360) currentTime (if (((currentTime - previousHit) * 30 + currentAngle - 180) `mod` 360) == 0 then total + 1 else total) limit
  | otherwise = countAll beats (currentTime + 1) currentAngle previousHit total limit


checkAny beats x = foldr (\ beat -> (||) ((x `mod` fst beat) == snd beat)) False beats
