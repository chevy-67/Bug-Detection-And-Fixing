async function submitCode() {
    const code = document.getElementById("codeInput").value;
    const output = document.getElementById("output");
    output.innerText = "Processing...";
  
    try {
      const response = await fetch("http://localhost:8000/fix-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_code: code })
      });
  
      const result = await response.json();
      if (response.ok) {
        output.innerText = result.suggested_fix;
      } else {
        output.innerText = "Error: " + result.detail;
      }
    } catch (err) {
      output.innerText = "Request failed: " + err.message;
    }
  }
  