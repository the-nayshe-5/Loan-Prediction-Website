document.getElementById('predictionForm').onsubmit = async function(event) {
    event.preventDefault();
    
    const data = {
        recovery_rate: parseFloat(document.getElementById('recovery_rate').value)/100,
        data: {
            credit_lines_outstanding: parseFloat(document.getElementById('credit_lines_outstanding').value),
            loan_amt_outstanding: parseFloat(document.getElementById('loan_amt_outstanding').value),
            total_debt_outstanding: parseFloat(document.getElementById('total_debt_outstanding').value),
            income: parseFloat(document.getElementById('income').value),
            years_employed: parseFloat(document.getElementById('years_employed').value),
            fico_score: parseFloat(document.getElementById('fico_score').value)
        }
    };

    const response = await fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    
    // Display results in modal
    document.getElementById('resultText').innerText = `
        Predicted to Default Loan?: ${result.prediction}, 
        Expected Loss Value: Rs. ${result.expected_loss}, 
        Probability of Default: ${result.probability_of_default}`;
    
    // Show modal
    document.getElementById('resultModal').style.display = "block";
};

// Modal close functionality
const modal = document.getElementById("resultModal");
const span = document.getElementsByClassName("close")[0];

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}