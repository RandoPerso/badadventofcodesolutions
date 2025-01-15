import System.IO
import qualified Data.Map as Map
import qualified Data.Char as Char

main = do
    inputFile <- openFile "2018/inputs/day_14_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let recipeRequirement = read contents :: Int
    let initialList = Map.fromList [(0, 3), (1, 7)]
    let finalRecipes = iterateUntil initialList 1 0 1 (recipeRequirement + 9)
    putStrLn $ map (Char.intToDigit . getValue finalRecipes) [recipeRequirement..recipeRequirement+9]
    putStrLn "This will take a bit..."
    let requirementList = map (\x -> read [x]) $ show recipeRequirement :: [Int]
    print $ iterateWhile initialList 1 0 1 requirementList
    putStrLn "done!"

iterateUntil listMap pointer elf1 elf2 goal
    | pointer >= goal = listMap
    | otherwise = iterateUntil newListMap newPointer newElf1 newElf2 goal
    where (newListMap, newPointer, newElf1, newElf2) = getNextState listMap pointer elf1 elf2

iterateWhile listMap pointer elf1 elf2 goal
    | pointer > 7 && check listMap (pointer - length goal) goal = pointer - length goal
    | pointer > 7 && check listMap (pointer - length goal + 1) goal = pointer - length goal + 1
    | otherwise = iterateWhile newListMap newPointer newElf1 newElf2 goal
    where (newListMap, newPointer, newElf1, newElf2) = getNextState listMap pointer elf1 elf2

getNextState listMap pointer elf1 elf2 = (newListMap, newPointer, newElf1, newElf2)
    where thisSum = getValue listMap elf1 + getValue listMap elf2
          newRecipes = intToList thisSum
          newListMap = foldl (\x (index, value) -> insertValue x (pointer + index) value) listMap (zip [0..] newRecipes)
          newPointer = pointer + length newRecipes
          newElf1 = (elf1 + 1 + getValue listMap elf1) `mod` (newPointer + 1)
          newElf2 = (elf2 + 1 + getValue listMap elf2) `mod` (newPointer + 1)

check listMap pointer goal = map (getValue listMap) [pointer..pointer + length goal - 1] == goal

{-
insertValue linkedList pointer value = Map.insert (pointer + 1) (value, 1) $ Map.insert pointer (x, pointer + 1) linkedList
    where (x, _) = linkedList Map.! pointer

getNext linkedList pointer = snd $ linkedList Map.! pointer

getNextN _ pointer 0 = pointer
getNextN linkedList pointer times = getNextN linkedList (getNext linkedList pointer) (times - 1)

getValue linkedList pointer = fst $ linkedList Map.! pointer
-}

getValue = (Map.!)

insertValue listMap pointer value = Map.insert (pointer + 1) value listMap

intToList x
    | x < 10 = [x]
    | otherwise = [x `div` 10, x `mod` 10]