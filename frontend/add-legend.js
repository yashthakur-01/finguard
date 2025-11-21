// This script adds the Legend component to the pie chart in App.js
const fs = require('fs');
const path = require('path');

const appJsPath = path.join(__dirname, 'src', 'App.js');
let content = fs.readFileSync(appJsPath, 'utf8');

// Find and replace the section with the Legend added
const searchPattern = `                      </Pie>
                      <Tooltip formatter={(value) => formatCurrency(value)} />`;

const replacement = `                      </Pie>
                      <Legend layout="horizontal" verticalAlign="bottom" align="center" />
                      <Tooltip formatter={(value) => formatCurrency(value)} />`;

if (content.includes(searchPattern)) {
    content = content.replace(searchPattern, replacement);

    // Also update the chart height and vertical position
    content = content.replace(
        'height={300}>\r\n                    <PieChart>\r\n                      <Pie\r\n                        data={categorySummary}\r\n                        dataKey="amount"\r\n                        nameKey="category"\r\n                        cx="50%"\r\n                        cy="50%"',
        'height={360}>\r\n                    <PieChart>\r\n                      <Pie\r\n                        data={categorySummary}\r\n                        dataKey="amount"\r\n                        nameKey="category"\r\n                        cx="50%"\r\n                        cy="45%"'
    );

    fs.writeFileSync(appJsPath, content, 'utf8');
    console.log('✅ Successfully added Legend to pie chart!');
    console.log('✅ Updated chart height to 360px and adjusted vertical position');
} else {
    console.log('❌ Could not find the target pattern in App.js');
    console.log('The file may have already been modified or has a different structure.');
}
