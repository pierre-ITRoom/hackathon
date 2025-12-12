# Fichiers Exemples pour Import

Ce dossier contient des fichiers exemples pour tester les fonctionnalités d'import de l'API.

## Fichiers disponibles

### 1. competences.csv
Fichier CSV contenant 20 compétences pour 6 développeurs différents.

**Utilisation :**
```bash
curl -X POST http://localhost:5000/import/competences/csv \
  -F "file=@examples/competences.csv"
```

### 2. competences.json
Fichier JSON contenant 7 compétences (version JSON du CSV simplifié).

**Utilisation :**
```bash
curl -X POST http://localhost:5000/import/competences/json \
  -F "file=@examples/competences.json"
```

### 3. projets.json
Fichier JSON contenant 6 projets avec leurs équipes et technologies.

**Utilisation :**
```bash
curl -X POST http://localhost:5000/import/projects/json \
  -F "file=@examples/projets.json"
```

## Scénario de test complet

Pour tester l'application avec des données de démo :

1. Démarrer l'application :
   ```bash
   python app.py
   ```

2. Importer les compétences :
   ```bash
   curl -X POST http://localhost:5000/import/competences/csv \
     -F "file=@examples/competences.csv"
   ```

3. Importer les projets :
   ```bash
   curl -X POST http://localhost:5000/import/projects/json \
     -F "file=@examples/projets.json"
   ```

4. Vérifier les données :
   ```bash
   # Liste des collaborateurs
   curl http://localhost:5000/collaborators

   # Liste des technologies
   curl http://localhost:5000/technos

   # Liste des compétences
   curl http://localhost:5000/competences

   # Liste des projets
   curl http://localhost:5000/projects

   # Historique des projets
   curl http://localhost:5000/project_history
   ```

## Données contenues

### Collaborateurs (6)
- Jean Dupont
- Sophie Martin
- Luc Bernard
- Marie Durand
- Thomas Petit
- Emma Moreau

### Technologies (23+)
PHP, Symfony, React, MySQL, Python, Django, PostgreSQL, JavaScript, Node.js, MongoDB, Java, Spring Boot, Angular, C#, .NET, SQL Server, React Native, TypeScript, Firebase, Express, JWT, WPF, etc.

### Projets (6)
1. Site E-commerce (PHP/Symfony/React)
2. API REST Entreprise (Node.js/MongoDB)
3. Application Mobile Fitness (React Native)
4. Plateforme SaaS RH (Java/Spring Boot/Angular)
5. Application Desktop Gestion (C#/.NET)
6. Dashboard Analytics (Python/Django/React)

## Utilisation depuis React (frontend)

Pour utiliser ces imports depuis une application React :

```javascript
// Import de compétences CSV
const uploadCompetencesCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:5000/import/competences/csv', {
    method: 'POST',
    body: formData
  });

  return await response.json();
};

// Import de projets JSON
const uploadProjectsJSON = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:5000/import/projects/json', {
    method: 'POST',
    body: formData
  });

  return await response.json();
};

// Utilisation avec un input file
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  const result = await uploadCompetencesCSV(file);
  console.log(`Créées: ${result.created}, Mises à jour: ${result.updated}`);
};
```

## Composant React exemple

```jsx
import React, { useState } from 'react';

function FileUploader() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (event, endpoint) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Import de données</h2>

      <div>
        <label>Compétences CSV:</label>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => handleUpload(e, '/import/competences/csv')}
          disabled={loading}
        />
      </div>

      <div>
        <label>Compétences JSON:</label>
        <input
          type="file"
          accept=".json"
          onChange={(e) => handleUpload(e, '/import/competences/json')}
          disabled={loading}
        />
      </div>

      <div>
        <label>Projets JSON:</label>
        <input
          type="file"
          accept=".json"
          onChange={(e) => handleUpload(e, '/import/projects/json')}
          disabled={loading}
        />
      </div>

      {loading && <p>Import en cours...</p>}

      {result && (
        <div>
          <h3>Résultat:</h3>
          <p>{result.message}</p>
          {result.created && <p>Créés: {result.created}</p>}
          {result.updated && <p>Mis à jour: {result.updated}</p>}
          {result.created_projects && <p>Projets créés: {result.created_projects}</p>}
          {result.created_history && <p>Historiques créés: {result.created_history}</p>}
          {result.errors && result.errors.length > 0 && (
            <div>
              <h4>Erreurs:</h4>
              <ul>
                {result.errors.map((err, idx) => (
                  <li key={idx}>{err}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default FileUploader;
```
