import sys

from src.db.Database import regexDatabase
from src.db.DbUtils import ABSTRACT_DOCUMENT, createTasks, TASKS_DOCUMENT
from src.pdf_processing.utils.SentenceTokenizer import SENTENCE_SPLITTER


def tagSentences(updateExisting=False):
    taskAbstracts = regexDatabase.find({ABSTRACT_DOCUMENT: {"$regex": "uzdevumi:"}})

    for record in taskAbstracts:
        if TASKS_DOCUMENT in record:
            print("already present!")
            if not updateExisting:
                continue
        record.update(createTasks(list()))
        taskAbstractProcessed = record[ABSTRACT_DOCUMENT]
        abstractSentences = SENTENCE_SPLITTER.tokenize(taskAbstractProcessed)
        for idx, abstractSentence in enumerate(abstractSentences):
            clearConsole()
            print(abstractSentence)
            choice = get_user_choice()
            if choice is None:
                break
            if choice:
                presentTasks = record[TASKS_DOCUMENT]
                presentTasks.append([idx, abstractSentence.strip()])
                regexDatabase.save(record)


def get_user_choice():
    print()
    print("[y] Save sentence.")
    print("[n] Skip sentence.")
    print("[s] Skip this document.")
    print("[q] Quit.")

    userInput = input("What would you like to do? ").lower()
    if "y" == userInput:
        return True
    elif "n" == userInput:
        return False
    elif "s" == userInput:
        return None
    elif "q" == userInput:
        sys.exit()
    return


def clearConsole():
    print('\n' * 25)
    # os.system('cls' if os.name == 'nt' else 'clear')


# Sentence unable to detect
# Pētījumam izvirzīti trīs darba uzdevumi: - noskaidrot, kādus profesionāļus laikraksti aicina izteikties par politisko komunikāciju (ko laikraksti nodēvē par politiskās komunikācijas ekspertiem); - noskaidrot, kāds ir politiskās komunikācijas diskurss ekspertu vēstījumos, - konstatēt vai politiskās komunikācijas diskurss ekspertu vēstījumos satur racionalitātes pazīmes.
# Bakalaura darba mērķis ir pamatojoties uz mārketinga stratēģijas plānošanas teorētiskajām atziņām un uzņēmuma “ Profs Latvija” mārketinga vides analīzi, izstrādāt priekšlikumus uznēmuma mārketinga stratēģijas pilnveidošanai Bakalaura darba uzdevumi: 1.  izskatīt mārketinga stratēģijas plānošanas teorētiskos aspektus; 2.  izanalizēt stratēģijas izvēles modeļus; 3.  izanalizēt uzņēmuma “Profs Latvija” mārketinga vides faktorus un to ietekmi uz uzņēmuma mārketinga stratēģijas izvēli; 4.  izpētīt uzņēmuma “ Profs Latvija” attīstības mērķus tuvā, vidējā un ilgā termiņā; 5.  izstrādāt priekšlikumus uznēmuma mārketinga stratēģijas pilnveidošanai.
# Lai sasniegtu izvirzīto mērķi, tika izdalīti trīs pamatuzdevumi: aplūkot Latvijas valdības realizēto politiku attiecībā pret PB; izanalizēt Vidzemes latviešu draudžu materiālo stāvokli, kā arī pievērsties situācijai draudžu klērā un draudžu garīgās dzīves attīstībai.
# Ma{istra darba uzdevumi: - apzināt un izvērtēt pašaktīvas pašvaldības iespējas integrētas vides sadarbības programmas izstrādē un ieviešanā Latvijā; - izvērtēt Līvānu novada pašvaldības pašreizējo vides pārvaldības cilvēkresursu kapacitāti un salīdzināt to ar citām pašvaldībām Latvijā un Baltijas jūras re{ionā; - izanalizēt dažādu līdz šim Līvānu novadā ieviesto pasākumu efektivitāti vides pārvaldības cilvēkresursu attīstības jomā;  - veikt labākās prakses (best practice) apkopojumu un gadījumu salīdzinošo analīzi (case study) Baltijas jūras re{ionā un Latvijā; - izstrādāt Līvānu novada pašaktīvas pašvaldības integrētas vides sadarbības vadlīnijas.
# Pamatojoties uz darba mērķi, tika izvirzīti sekojoši uzdevumi: 1) izpētīt tēmai atbilstošu pedagoģisko, psiholoģisko, didaktisko literatūru; 2) analizēt skolēnu priekšstatu par valodas stilu, funkcionālajiem stiliem; 3) izmantojot teorētiskajos pētījumos iegūto pieredzi, izvēlēties un apkopot uzdevumus, kura mērķis ir stilistisko prasmju pilnveidošana; 4) aprobēt uzdevumus praksē, konstatēt skolēnu sasniegumus, veikt secinājumus skolēnu stilistiskajās prasmēs.
# Lai sasniegtu šo mērķi, jārealizē šādi uzdevumi: 1.  iepazīties ar teorētiskām nostādnēm par priekšmetiskās vides izveidi pirmskolā; 2.  izzināt rotaļnodarbību organizēšanu aktivitāšu centros pirmskolā; 3.  veikt rotaļnodarbību programmas izveidi un izvērtējumu.
# Darba sākumā tika izvirzīti šādi darba uzdevumi: teorētiskās literatūras apkopošana par partijām, to funkcijām, veidiem un veidošanās īpatnībām jaunajās demokrātiskajās valstīs un vēlēšanu būtību; aplūkot partijas TB/LNNK veidošanos; partijas programmu iegūšana un satura analīze; partijas TB/LNNK ietekmes 7. , 8. , 9.
# Izstrādājot darbu tika veikti vairāki uzdevumi:  (cid:190) apskatīta projekta pārvaldības zināšanu kopuma metodoloģija: definīcijas, projekta pārvaldības konteksts, projekta pārvaldības zināšanu apgabali, projekta pārvaldības procesi un procesu grupas,  (cid:190) projekta pārvaldības zināšanu kopuma metodoloģija pielāgota projekta „Interneta veikals RigaShop” pārvaldes specifikai, (cid:190) balstoties uz pielāgoto metodiku tika izstrādāts projekta plāns, (cid:190) projekts izpildīts pēc iepriekšnodefinēta projekta plāna.
# Lai sasniegtu darba mērķi, tika izvirzīti vairāki uzdevumi: 1.  raksturot valūtas sistēmas attīstības posmi un tas pakāpeniskas izmaiņas;  2.  raksturot Monetārās sistēmas attistību; 3.  izpētīt eiro ieviešanas Latvijā riskus un iespējas; 4.  izdarīt secinājumus par Latvijas gatavību eiro ieviešanai un izvirzīt priekšlikumus Darbs sastāv no trīm nodaļām, secinājumiem un priekšlikumiem, kā arī izmantotās literatūras saraksta.

if __name__ == '__main__':
    tagSentences()
