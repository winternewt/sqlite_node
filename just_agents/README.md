# Using in junction with just-agents

## Quickstart

- Download [Drugage](https://genomics.senescence.info/download.html#drugage) database as a `.csv` file 
- Rename it to `database.csv`, place into `data/database.csv` folder in the root of this repo.
- Deploy the SQLite node following the instructions of the repository readme
- Create `.env` file, place your `OPENAI_API_KEY=sk-proj-...` there.
- Install `just-agents` as instructed by [Just-agents](https://github.com/longevity-genie/just-agents) repo, TL;DR:
``` commandline
pip install just-agents
```
- Run the test
``` commandline
python test_query.py 
```

## Expected output
Below is a sample of the correctly executed query, utilizing both tools. Note that tools description is not self-sufficient,  
prompt engineering is still necessary for LLMs to utilize them properly.

```
$python3 ./just_agents/test_query.py 
TOOL HEADERS was used
TOOL QUERY was used with SELECT DISTINCT model_animal FROM csv_data
TOOL QUERY was used with SELECT DISTINCT species FROM csv_data
Results:  The **DrugAge** database contains the following columns:

1. **compound_name**
2. **cas_number**
3. **species**
4. **strain**
5. **dosage**
6. **avg_lifespan_change**
7. **max_lifespan_change**
8. **gender**
9. **significance**
10. **pubmed_id**

### Model Animals
The model animals listed in the database include:

- Drosophila mojavensis
- Drosophila melanogaster
- Caenorhabditis elegans
- Rattus norvegicus
- Mus musculus
- Mytilina brevispina
- Mesocricetus auratus
- Asplanchna brightwelli
- Musca domestica
- Zaprionus paravittiger
- Aedes aegypti
- Philodina acuticornis
- Drosophila bipectinata
- Canis lupus familiaris
- Paramecium tetraurelia
- Saccharomyces cerevisiae
- Nothobranchius furzeri
- Ceriodaphnia affinis
- Podospora anserina
- Anastrepha ludens
- Apis mellifera
- Nothobranchius guentheri
- Tribolium castaneum
- Brachionus manjavacas
- Daphnia pulex clone TCO
- Aeolosoma viride
- Acheta domesticus
- Anopheles stephensi
- Bombyx mori
- Drosophila virilis
- Drosophila kikkawai
- Adineta vaga
- Caenorhabditis briggsae
- Caenorhabditis tropicalis
- Aedes albopictus

These species are commonly used in research related to aging and lifespan studies.
TOOL QUERY was used with SELECT species, MAX(avg_lifespan_change) as max_lifespan_effect FROM csv_data WHERE compound_name = 'Metformin' GROUP BY species ORDER BY max_lifespan_effect DESC LIMIT 1;
Results:  The internal name of the DrugAge database is **csv_data**. 

The animal model in which the lifespan effect of metformin was maximal is **Acheta domesticus**, with a maximum lifespan effect of **79.0**.
```

## Contents
- `ai_tools.py`: The Tools enabling AI to communicate with a DB via REST API.
- `test_query.py`: An example query to a [Drugage](https://genomics.senescence.info/download.html#drugage) database imported as a `.csv` file 

