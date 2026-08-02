## Inspiration
We saw how  nurses suffer from physical burnout by having to visit a patient’s bedside three to four times a day. But, building a tool only for nurses is not economically good for hospitals. To solve this, we created **MediFlow** with Inbuilt AI.
## What it does
* **Unified Staff Workspace**: _MediFlow_ streamlines hospital operations by connecting the reception desk, nursing triage, and doctors into a single digital web.
* **Smart Patient Registration**: Allows the reception desk to easily  register new patients or look up profiles of returning patients.
* **AI-Driven Medical Web**: Analyzes initial nursing observations and patient symptoms to intelligently recommend the best-suited specialist or department, Then helps the doctor also in giving treatment .
* **Automated Doctor Routing**: Instantly routes the patient's digital file to the suggested doctor's queue, drastically reducing wait times.
* **Clinical Activity tracker** : Tracks real-time patient status updates to eliminate redundant bedside check-ins by nursing staff.

## How we built it
* **Backend Framework**:  Built using  Python to manage clinical data processing and state routing.
* **User Interface**: Crafted using Streamlit to quickly deploy a highly functional, multi-page staff dashboard.
* **Database Engine**: Structured around an SQLite3 database to store and link patient records, staff accounts, and visit logs locally.
* **AI Engine Integration**: Connected an AI Language Model( Groq) to process unstructured clinical text notes and return instant specialist recommendations.

## Challenges we ran into
* **Streamlit State Management**: Streamlit reruns the entire script on user interaction. We struggled to keep patient data locked in place when switching views between the receptionist, nurse, and doctor dashboards inside MediFlow.
* **Deployment**: Running a stateful application connected to a live database file presented multiple hosting blocks during our cloud deployment attempts. 

## Accomplishments that we're proud of
* **Real-World Impact**: Identified a severe healthcare bottleneck and engineered a tool that directly protects nurses from administrative burnout.
* **Built Fully Working Web app**: Successfully built an end-to-end web app that connects a patient from registration to the doctor's screen in real time.
* **Accessible Tech Assembly**: Rapidly learned and combined Streamlit, Python, and AI capabilities under a very tight hackathon clock.Multi-User Simulation: Successfully demonstrated how different roles 

## What we learned
* **Full-Stack Prototyping**: How to use Streamlit to rapidly assemble data-driven dashboards without deep frontend experience
* **AI Usage**: How to pass custom prompt contexts to an AI model to get accurate, domain-specific medical routing suggestions.
* **Data Mapping**: Designing database tables that cleanly connect patients to specific visits, observations, and doctors.

## What's next for Hospital Management system with Ai inbuilt
* **Shift from Streamlit**: Migrate the entire application to a FastAPI (Backend) and React (Frontend) stack to handle heavy hospital user traffic and improve the UI.
* **Advanced AI Features**: Train the AI to read uploaded medical scans (X-rays/MRIs) and automatically calculate an emergency triage priority score.
* **Mobile Deployment**: Launch a mobile or tablet version of MediFlow so nurses can update patient charts directly at the bedside.
**Consumers**: Deploy a free  to a local community clinic to find our first real-world clients and healthcare users.
