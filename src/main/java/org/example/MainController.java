package org.example;

import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;
import org.example.NewsCrawler;

public class MainController {
    public static void main(String[] args) throws Exception {
        String crawlStorageFolder = "data/crawl/root"; // Directory where intermediate crawl data will be stored
        int numberOfCrawlers = 7; // Number of concurrent threads

        // Configure the crawler settings
        CrawlConfig config = new CrawlConfig();
        config.setCrawlStorageFolder(crawlStorageFolder);
        config.setMaxDepthOfCrawling(16);
        config.setMaxPagesToFetch(20000);
        config.setPolitenessDelay(200); // Delay between requests

        // Instantiate required components for CrawlController
        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);

        // Create the CrawlController
        CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);

        // Set seed URL based on your assignment
        controller.addSeed("https://www.foxnews.com/");

        // Start crawling using the NewsCrawler class
        controller.start(NewsCrawler.class, numberOfCrawlers);
    }
}