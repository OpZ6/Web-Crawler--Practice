package org.example;

import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;
import org.apache.http.HttpStatus;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Set;
import java.util.regex.Pattern;

public class NewsCrawler extends WebCrawler {

    // Patterns to filter out files that we do not want to crawl
    private static final Pattern EXCLUSIONS = Pattern.compile(".*(\\.(css|js|gif|jpg|png|mp3|mp4|zip|gz))$");

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        String href = url.getURL().toLowerCase();
        // Only visit pages that belong to the Fox News domain
        return !EXCLUSIONS.matcher(href).matches() && href.startsWith("https://www.foxnews.com");
    }

    @Override
    public void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
        String url = webUrl.getURL();
        // Save the fetched URL and HTTP status code, with header row if the file is empty
        File fetchFile = new File("fetch_foxnews.csv");
        boolean isFetchFileEmpty = !fetchFile.exists() || fetchFile.length() == 0;
        try (FileWriter fetchWriter = new FileWriter(fetchFile, true)) {
            if (isFetchFileEmpty) {
                fetchWriter.append("URL,Status Code\n");
            }
            fetchWriter.append(url).append(",").append(String.valueOf(statusCode)).append("\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void visit(Page page) {
        String url = page.getWebURL().getURL();
        System.out.println("Visiting: " + url);

        if (page.getParseData() instanceof HtmlParseData) {
            HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
            String text = htmlParseData.getText();
            String html = htmlParseData.getHtml();
            Set<WebURL> outgoingUrls = htmlParseData.getOutgoingUrls();
            int outlinksCount = outgoingUrls.size();
            String contentType = page.getContentType() != null ? page.getContentType().split(";")[0] : "unknown";

            // Save the crawl data into visit CSV file, with header row if the file is empty
            File visitFile = new File("visit_foxnews.csv");
            boolean isVisitFileEmpty = !visitFile.exists() || visitFile.length() == 0;
            try (FileWriter visitWriter = new FileWriter(visitFile, true)) {
                if (isVisitFileEmpty) {
                    visitWriter.append("URL,Size (bytes),Number of Outlinks,Content Type\n");
                }
                visitWriter.append(url)
                        .append(',')
                        .append(String.valueOf(page.getContentData().length))
                        .append(',')
                        .append(String.valueOf(outlinksCount))
                        .append(',')
                        .append(contentType)
                        .append('\n');
            } catch (IOException e) {
                e.printStackTrace();
            }

            // Save discovered URLs, with header row if the file is empty
            File urlsFile = new File("urls_foxnews.csv");
            boolean isUrlsFileEmpty = !urlsFile.exists() || urlsFile.length() == 0;
            try (FileWriter urlsWriter = new FileWriter(urlsFile, true)) {
                if (isUrlsFileEmpty) {
                    urlsWriter.append("Discovered URL,Is Internal\n");
                }
                for (WebURL webURL : outgoingUrls) {
                    String link = webURL.getURL();
                    String isInternal = link.startsWith("https://www.foxnews.com") ? "OK" : "N_OK";
                    urlsWriter.append(link).append(",").append(isInternal).append("\n");
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}