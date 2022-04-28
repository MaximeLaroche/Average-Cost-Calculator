# Instructions pour faire fonctionner le logiciel pour disnat
Commencez par télécharger les données et les copier dans le disnat.csv (pour mettre les nouvelles données avec les vieilles)

# Ajustement des données
## Changement de nom
Quand une actions change de symbole, on doit manuellement entrer de l'info de plus pour que le logiciel puisse associer les vieux ticker avec le nouveux.
- Filtrer pour 'ECH - Actions' dans le document csv
  - Dans la colone Symbole, entrez le vieux symbole
  - Dans la colone description, entrez le nouveaux symbole. Si il y a déjà de quoi dans la description, remplacer le contenu par le nouveau symbole

## Faillite
- Entrer le symbole dans la rangé Symbole. Ça sera compté comme vente à 0$

## Transferts
- Pour l'instants, uniquement les transferts du 20 décembre 2019 sont prix en considération. Il faut que le symbole et le prix soit entré manuellement