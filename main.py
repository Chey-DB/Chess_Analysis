from data_extractor import ChessDataExtractor
from data_analyser import ChessDataAnalyser


if __name__ == "__main__":
    extractor = ChessDataExtractor("cheydb", "cheydb@rocketmail.com")
    print(extractor.get_monthly_archive_urls())
