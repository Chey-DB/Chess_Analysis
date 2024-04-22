from data_extractor import ChessDataExtractor


if __name__ == "__main__":
    extractor = ChessDataExtractor("cheydb", "cheydb@rocketmail.com")
    print(extractor.get_monthly_archive_urls())
