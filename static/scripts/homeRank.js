let rankingSelection = 'gdp-rank-btn';
const rankingOptions = ['gdp-rank-btn', 'inflation-rank-btn', 'equality-rank-btn'];
const rankingDivs = ['gdp-rank', 'inflation-rank', 'equality-rank']

// Iterate through each button ID
for (const id of rankingOptions) {
    let button = document.getElementById(id);

    // Add a click event listener to each button
    button.addEventListener('click', () => {

        rankingSelection = button.id;
        // Remove 'bg-blue-500' class from all buttons
        for (const uid of rankingOptions) {
            const item = document.getElementById(uid);
            item.classList.remove('bg-blue-500');
        }

        for (const div of rankingDivs) {
            const item = document.getElementById(div)
            item.classList.add('hidden')
        }

        // Add 'bg-blue-500' class to the clicked button
        button.classList.add('bg-blue-500');

        // Show desired box for ranking
        if (rankingSelection === 'gdp-rank-btn') document.getElementById('gdp-rank').classList.remove('hidden')
        else if (rankingSelection === 'equality-rank-btn') document.getElementById('equality-rank').classList.remove('hidden')
        else if (rankingSelection === 'inflation-rank-btn') document.getElementById('inflation-rank').classList.remove('hidden')


    });
}
