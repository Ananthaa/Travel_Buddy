document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('travelForm');
    const steps = document.querySelectorAll('.form-step');
    const nextBtns = document.querySelectorAll('.btn-next');
    const prevBtns = document.querySelectorAll('.btn-prev');
    const submitBtn = document.querySelector('.btn-submit');

    let currentStep = 0;

    function showStep(stepIndex) {
        steps.forEach((step, index) => {
            step.classList.remove('active');
            if (index === stepIndex) {
                step.classList.add('active');
            }
        });
    }

    function validateStep(stepIndex) {
        const currentStepEl = steps[stepIndex];
        const inputs = currentStepEl.querySelectorAll('input, select');
        let isValid = true;

        inputs.forEach(input => {
            if (input.hasAttribute('required') && !input.value) {
                isValid = false;
                input.style.borderColor = '#ef4444';
                // Shake animation
                input.animate([
                    { transform: 'translateX(0)' },
                    { transform: 'translateX(-5px)' },
                    { transform: 'translateX(5px)' },
                    { transform: 'translateX(0)' }
                ], {
                    duration: 300
                });
            } else {
                input.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            }
        });

        return isValid;
    }

    nextBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                currentStep++;
                showStep(currentStep);
            }
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentStep--;
            showStep(currentStep);
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validateStep(currentStep)) return;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Change button text to loading
        const originalText = submitBtn.innerText;
        submitBtn.innerText = 'Planning...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                // Show success message with Generate Itinerary button
                form.innerHTML = `
                    <div style="text-align: center;">
                        <h2 style="color: #4ade80; margin-bottom: 1rem;">Success!</h2>
                        <p>${result.message}</p>
                        <p style="margin-top: 1rem; opacity: 0.7;">Your travel buddy is ready to build your itinerary.</p>
                        
                        <div id="generation-area" style="margin-top: 2rem;">
                            <button id="btn-generate" style="background: linear-gradient(to right, #ec4899, #8b5cf6); width: 100%;">Generate Itinerary with AI</button>
                        </div>
                        
                        <button onclick="location.reload()" style="margin-top: 1rem; background: rgba(255,255,255,0.1); width: 100%;">Plan Another Trip</button>
                    </div>
                `;

                // Add event listener for generation
                const genBtn = document.getElementById('btn-generate');
                const itinerarySection = document.getElementById('itinerary-section');
                const itineraryContent = document.getElementById('itinerary-content');
                const feedbackInput = document.getElementById('feedback-input');
                const updateBtn = document.getElementById('btn-update-itinerary');
                const finalizeBtn = document.getElementById('btn-finalize');
                const downloadArea = document.getElementById('download-area');

                async function fetchItinerary(feedback = null) {
                    const requestData = { ...data };
                    if (feedback) {
                        requestData.feedback = feedback;
                        requestData.current_itinerary = itineraryContent.innerText;
                    }

                    try {
                        const genResponse = await fetch('/generate_itinerary', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(requestData)
                        });

                        const genResult = await genResponse.json();

                        if (genResponse.ok) {
                            console.log('Received itinerary text, first 200 chars:', genResult.itinerary_text.substring(0, 200));

                            // Parse Markdown - this works for both initial and update
                            const parsedHTML = marked.parse(genResult.itinerary_text);
                            console.log('Parsed HTML, first 200 chars:', parsedHTML.substring(0, 200));

                            itineraryContent.innerHTML = parsedHTML;
                            itineraryContent.classList.add('markdown-content');
                            itinerarySection.style.display = 'block';

                            // Set dynamic image
                            const collageImg = document.getElementById('destination-collage');
                            const destination = data.destination || 'travel';
                            const imageUrl = `https://image.pollinations.ai/prompt/travel%20collage%20of%20${encodeURIComponent(destination)}%20attractions%20scenic%20view%20photorealistic?width=800&height=400&nologo=true`;
                            collageImg.src = imageUrl;
                            collageImg.style.display = 'block';

                            // Show feedback and finalize areas
                            document.getElementById('feedback-area').style.display = 'block';
                            document.getElementById('finalize-area').style.display = 'block';

                            // Scroll to itinerary
                            itinerarySection.scrollIntoView({ behavior: 'smooth' });

                            if (feedback) {
                                console.log('Update completed successfully');
                                updateBtn.innerText = 'Update Itinerary';
                                updateBtn.disabled = false;
                                feedbackInput.value = ''; // Clear feedback
                            } else {
                                console.log('Initial generation completed successfully');
                                genBtn.innerText = 'Regenerate Itinerary';
                                genBtn.disabled = false;
                            }
                        } else {
                            alert('Error generating itinerary: ' + genResult.message);
                            if (feedback) {
                                updateBtn.innerText = 'Update Itinerary';
                                updateBtn.disabled = false;
                            } else {
                                genBtn.innerText = 'Generate Itinerary with AI';
                                genBtn.disabled = false;
                            }
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Failed to generate itinerary.');
                        if (feedback) {
                            updateBtn.innerText = 'Update Itinerary';
                            updateBtn.disabled = false;
                        } else {
                            genBtn.innerText = 'Generate Itinerary with AI';
                            genBtn.disabled = false;
                        }
                    }
                }

                genBtn.addEventListener('click', async () => {
                    genBtn.innerText = 'Generating Itinerary... (This may take a moment)';
                    genBtn.disabled = true;
                    await fetchItinerary();
                });

                // Update Handler
                updateBtn.addEventListener('click', async () => {
                    const feedback = feedbackInput.value.trim();
                    if (!feedback) {
                        alert('Please enter some feedback first.');
                        return;
                    }
                    updateBtn.innerText = 'Updating...';
                    updateBtn.disabled = true;
                    await fetchItinerary(feedback);
                });

                // Finalize Handler
                finalizeBtn.addEventListener('click', async () => {
                    finalizeBtn.innerText = 'Finalizing...';
                    finalizeBtn.disabled = true;

                    const collageImg = document.getElementById('destination-collage');

                    try {
                        const finalizeResponse = await fetch('/finalize_itinerary', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                ...data,
                                itinerary_text: itineraryContent.innerText,
                                image_url: collageImg.src
                            })
                        });

                        const finalizeResult = await finalizeResponse.json();

                        if (finalizeResponse.ok) {
                            downloadArea.innerHTML = `
                                    <a href="${finalizeResult.pdf_url}" target="_blank" style="display: block; padding: 1rem; background: #4ade80; color: #0f172a; border-radius: 10px; text-decoration: none; font-weight: bold; text-align: center;">
                                        Download Itinerary PDF 📥
                                    </a>
                                `;
                            downloadArea.style.display = 'block';
                            finalizeBtn.innerText = 'Finalized!';
                        } else {
                            alert('Error finalizing itinerary: ' + finalizeResult.message);
                            finalizeBtn.innerText = 'Finalize & Download PDF';
                            finalizeBtn.disabled = false;
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Failed to finalize itinerary.');
                        finalizeBtn.innerText = 'Finalize & Download PDF';
                        finalizeBtn.disabled = false;
                    }
                });

            } else {
                alert('Error: ' + result.message);
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
            submitBtn.innerText = originalText;
            submitBtn.disabled = false;
        }
    });

    // Input focus effect reset
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            input.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        });
    });
});
