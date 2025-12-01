import System.IO
import qualified Data.Map as Map

main = do
    inputFile <- openFile "2018/inputs/day_24_2018_ex.txt" ReadMode
    contents <- hGetContents inputFile
    let initialState = (\f (a, b) -> (f a, f b)) createMap $ parse (tail $ lines contents) [] [] False
    putStrLn "done!"

createMap x = Map.fromList (map (\(a, b, c, d, e, initiative) -> (initiative, (a, b, c, d, e))) x)

damageDealt attacker@(_, _, _, _, damageType) (_, _, (immuneList, weakList), _, _)
    | damageType `elem` immuneList = 0
    | damageType `elem` weakList = currentEffectivePower * 2
    | otherwise = currentEffectivePower
    where currentEffectivePower = effectivePower attacker

effectivePower (numberOfUnits, _, _, damage, _) = numberOfUnits * damage

attacksMap = Map.fromList [("radiation", 0), ("fire", 1), ("cold", 2), ("slashing", 3), ("bludgeoning", 4)]

parse [] immuneList infectionList _ = (reverse immuneList, reverse infectionList)
parse (x:xs) immuneList infectionList False
    | x == "" = parse (tail xs) immuneList infectionList True
    | otherwise = parse xs (parseLine x : immuneList) infectionList False
parse (x:xs) immuneList infectionList True = parse xs immuneList (parseLine x : infectionList) True

parseLine line = (numberOfUnits, healthPoints, parseEffects temp, damage, damageType, initiative)
    where temp = words line
          numberOfUnits = read $ head temp :: Integer
          healthPoints = read $ temp !! 4 :: Integer
          damage = read $ temp !! (length temp - 6) :: Integer
          damageType = attacksMap Map.! (temp !! (length temp - 5))
          initiative = read $ temp !! (length temp - 1) :: Integer

parseEffects line = parseEffects2 semiParsedLine ([], []) True
    where semiParsedLine = weirdThing $ take (length line - 18) $ drop 7 line

parseEffects2 [] output _ = output
parseEffects2 (x:xs) output@(immuneList, weakList) onWeak
    | x == "weak" = parseEffects2 (tail xs) output True
    | x == "immune" = parseEffects2 (tail xs) output False
    | otherwise = parseEffects2 xs nextEffects True
    where temp = removeTrailingPunctuation x
          nextEffects = if onWeak then (immuneList, (attacksMap Map.! temp) : weakList) else ((attacksMap Map.! temp) : immuneList, weakList)

removeTrailingPunctuation x = if last x `elem` ",;" then init x else x

weirdThing x = tail (head x) : init (tail x) ++ [init (last x)]
