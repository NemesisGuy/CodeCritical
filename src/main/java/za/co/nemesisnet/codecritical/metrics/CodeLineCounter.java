package za.co.nemesisnet.codecritical.metrics;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class CodeLineCounter {
    private int totalLines = 0;
    private int totalCodeLines = 0;
    private int totalCommentLines = 0;
    private int totalFunctions = 0;
    private int totalClasses = 0; // Total classes counter
    private int totalInterfaces = 0; // Total interfaces counter
    private StringBuilder markdownContent = new StringBuilder();
    private StringBuilder emptyDirectories = new StringBuilder(); // Separate builder for empty directories
    private int fileCount = 0; // Keep track of the number of files
    private String baseDirectoryPath; // Base directory to use for relative paths

    public void countLines(String directoryPath) {
        File directory = new File(directoryPath);
        if (!directory.isDirectory()) {
            System.out.println("The provided path is not a directory.");
            return;
        }

        baseDirectoryPath = directory.getAbsolutePath(); // Store the base directory for relative paths
        processDirectory(directory);
    }

    private void processDirectory(File directory) {
        boolean hasJavaFiles = false; // Track if this directory has Java files
        String relativePath = directory.getAbsolutePath().replace(baseDirectoryPath, ".");

        // Create a temporary string builder for the current directory's markdown output
        StringBuilder currentDirMarkdown = new StringBuilder();
        currentDirMarkdown.append("\n## Directory: ").append(relativePath).append("\n\n");
        currentDirMarkdown.append("| # | File Name | Total Lines | Code Lines | Comment Lines | Function Count | Class Count | Interface Count | Duplicate Count | Maintainability Index | Cyclomatic Complexity |\n");
        currentDirMarkdown.append("|---|-----------|-------------|------------|---------------|----------------|-------------|------------------|------------------|------------------------|-----------------------|\n");

        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    processDirectory(file); // Recursively process subdirectories
                } else if (file.getName().endsWith(".java")) {
                    hasJavaFiles = true; // Mark that this directory has Java files
                    fileCount++; // Increment file count
                    countFileLines(file, currentDirMarkdown); // Pass the markdown builder for this directory
                }
            }
        }

        // Append the current directory's markdown content if it has Java files
        if (hasJavaFiles) {
            markdownContent.append(currentDirMarkdown);
        } else {
            emptyDirectories.append(" - ").append(relativePath).append("\n"); // Add to empty directories list
        }
    }

    private void countFileLines(File file, StringBuilder currentDirMarkdown) {
        int fileLines = 0;
        int fileCodeLines = 0;
        int fileCommentLines = 0;
        int fileFunctionCount = 0;
        int fileClassCount = 0;
        int fileInterfaceCount = 0;
        int totalCyclomaticComplexity = 0; // Initialize cyclomatic complexity

        StringBuilder fileContent = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            StringBuilder currentMethodBody = new StringBuilder();
            boolean inMethod = false;

            while ((line = reader.readLine()) != null) {
                fileLines++;
                totalLines++;

                fileContent.append(line).append("\n"); // Store content for duplication detection

                if (line.trim().isEmpty()) {
                    continue;
                }

                if (line.trim().startsWith("//") || line.trim().startsWith("/*") || line.trim().startsWith("*")) {
                    fileCommentLines++;
                    totalCommentLines++;
                } else {
                    fileCodeLines++;
                    totalCodeLines++;
                }

                // Check for function declarations
                if (line.trim().matches(".*(public|private|protected|static|final)\\s+.*\\(.*\\)\\s*\\{")) {
                    fileFunctionCount++;
                    totalFunctions++;
                    inMethod = true; // Start capturing method body
                    currentMethodBody.setLength(0); // Clear previous method body
                }

                if (inMethod) {
                    currentMethodBody.append(line).append("\n"); // Capture method body

                    // Check for method closing brace
                    if (line.contains("}")) {
                        // Calculate cyclomatic complexity for the method
                        CyclomaticComplexityCalculator cyclomaticComplexityCalculator = new CyclomaticComplexityCalculator();
                        totalCyclomaticComplexity += cyclomaticComplexityCalculator.calculate(currentMethodBody.toString());
                        currentMethodBody.setLength(0); // Reset for next method
                        inMethod = false; // End capturing method body
                    }
                }

                // Check for class and interface declarations
                if (line.trim().matches(".*\\b(class|interface)\\s+.*")) {
                    if (line.contains("class")) {
                        fileClassCount++;
                        totalClasses++;
                    } else if (line.contains("interface")) {
                        fileInterfaceCount++;
                        totalInterfaces++;
                    }
                }
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + file.getAbsolutePath());
            e.printStackTrace();
        }

        // Detect duplicates
        CodeDuplicationDetector duplicationDetector = new CodeDuplicationDetector();
        int duplicateCount = duplicationDetector.detectDuplicates(fileContent.toString());

        // Calculate Maintainability Index
        MaintainabilityIndexCalculator maintainabilityIndexCalculator = new MaintainabilityIndexCalculator();
        double maintainabilityIndex = maintainabilityIndexCalculator.calculateMaintainabilityIndex(fileCodeLines, fileFunctionCount, fileCommentLines);

        // Append to the markdown content for the current directory
        currentDirMarkdown.append(String.format("| %d | %s | %d | %d | %d | %d | %d | %d | %d | %.2f | %d |\n",
                fileCount, file.getName(), fileLines, fileCodeLines, fileCommentLines, fileFunctionCount, fileClassCount, fileInterfaceCount, duplicateCount, maintainabilityIndex, totalCyclomaticComplexity));
    }

    public void printGrandTotals() {
        markdownContent.append("\n");
        markdownContent.append("## Grand Totals\n\n");
        markdownContent.append("| Total Files | Grand Total Lines | Grand Total Code Lines | Grand Total Comment Lines | Grand Total Functions | Grand Total Classes | Grand Total Interfaces |\n");
        markdownContent.append("|-------------|-------------------|------------------------|---------------------------|-----------------------|---------------------|------------------------|\n");
        markdownContent.append(String.format("| %d | %d | %d | %d | %d | %d | %d |\n", fileCount, totalLines, totalCodeLines, totalCommentLines, totalFunctions, totalClasses, totalInterfaces));

        // Add empty directories section
        markdownContent.append("\n## Empty Directories\n\n");
        if (emptyDirectories.length() == 0) {
            markdownContent.append("None\n");
        } else {
            markdownContent.append(emptyDirectories);
        }
    }

    public void writeToFile(String filePath) {
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(markdownContent.toString());
            System.out.println("Results successfully written to " + filePath);
        } catch (IOException e) {
            System.err.println("Error writing to file: " + filePath);
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        CodeLineCounter counter = new CodeLineCounter();
        // Replace the path below with your actual path
        counter.countLines("src/main");

        // Call to print the grand totals only once after processing all files
        counter.printGrandTotals();

        // Write the results to the markdown file
        counter.writeToFile("CodeCounterResults.md");
    }
}
