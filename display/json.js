    const output = document.getElementById('output');

    document.getElementById('fileInput').addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(event) {
        try {
          const json = JSON.parse(event.target.result);
          output.innerHTML = '';
          const keysToDisplay = ['name','all_merged_reviews', 'courses', 'teaches', 'date_summarized']; // Customize here

          if (Array.isArray(json)) {
            json.forEach(item => output.appendChild(formatData(item, keysToDisplay)));
          } else {
            output.appendChild(formatData(json, keysToDisplay));
          }
        } catch {
          output.textContent = 'Invalid JSON file.';
        }
      };
      reader.readAsText(file);
    });

    function formatData(data, keys) {
      const container = document.createElement('div');
      container.className = 'data';
      keys.forEach(key => {
        const div = document.createElement('div');
        div.className = 'pair';
        div.innerHTML = `<span class="key">${key}:</span> ${data[key] ?? 'N/A'}`;
        container.appendChild(div);
      });
      return container;
    }
