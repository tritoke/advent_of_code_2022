{-# LANGUAGE TypeApplications #-}

import Control.Monad
import Control.Arrow
import Data.List
import Data.Maybe

type Range = (Int, Int)
type SectionAssignment = (Range, Range)

splitAtIndex :: Int -> [a] -> ([a], [a])
splitAtIndex index list = (take index list, drop (index + 1) list)

splitOnChar :: Char -> String -> (String, String)
splitOnChar c s = splitAtIndex index s
  where
    index = fromJust $ findIndex (== c) s

mapTuple :: Arrow a => a b' c' -> a (b', b') (c', c')
mapTuple = join (***)

parseInput :: String -> SectionAssignment
parseInput = mapTuple (mapTuple read . splitOnChar '-') . (splitOnChar ',')

rangesFullyOverLap :: SectionAssignment -> Bool
rangesFullyOverLap ((a, b), (c, d)) = a <= c && b >= d || c <= a && d >= b

rangesOverLap :: SectionAssignment -> Bool
rangesOverLap ((a, b), (c, d)) = not (c > b || d < a)

part :: (SectionAssignment -> Bool) -> String -> String
part pred = show . length . filter pred . map parseInput . lines

part1 :: String -> String
part1 = part rangesFullyOverLap

part2 :: String -> String
part2 = part rangesOverLap

solve :: String -> String
solve s = part1 s ++ '\n' : part2 s

main :: IO ()
main = join . liftM (putStrLn . solve) . readFile $ "input"

-- as a oneliner because it was funny
-- main = join . liftM (putStrLn . (\s -> (show . length . filter (\((a, b), (c, d)) -> a <= c && b >= d || c <= a && d >= b) . map ((join (***)) ((join (***)) (\x -> read @Int x) . (\s -> (\index list -> (take index list, drop (index + 1) list)) (fromJust $ findIndex (== '-') s) s)) . ((\s -> (\index list -> (take index list, drop (index + 1) list)) (fromJust $ findIndex (== ',') s) s))) . lines) s ++ '\n' : (show . length . filter (\((a, b), (c, d)) -> not (c > b || d < a)) . map ((join (***))((join (***)) (\x -> read @Int x) . (\s -> (\index list -> (take index list, drop (index + 1) list)) (fromJust $ findIndex (== '-') s) s)) . ((\s -> (\index list -> (take index list, drop (index + 1) list)) (fromJust $ findIndex (== ',') s) s))) . lines) s)) . readFile $ "input"

